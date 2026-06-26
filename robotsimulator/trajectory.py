"""
RobotSimulator — Trajectory Generator

Generates the complete X-Z swabbing trajectory for a FANUC robot
on the blank side of an IS hollow glass forming machine.

The trajectory follows these segments:
    1. WAIT    — Safe position above all obstacles
    2. APPROACH — Move down toward mould entry
    3. ENTER   — Move into the swabbing corridor (avoiding obstacles)
    4. SWAB_DOWN — Spray coating while moving down inside mould
    5. SWAB_UP   — (Optional) Spray coating while moving up inside mould
    6. EXIT    — Move out of the mould
    7. Return to WAIT position

All coordinates in millimeters.
"""

from __future__ import annotations

import math
import numpy as np
from typing import List, Optional, Tuple

from .models import (
    MouldGeometry,
    ObstacleEnvelope,
    RobotParameters,
    SwabbingParameters,
    TrajectoryPoint,
    TrajectoryResult,
    SegmentType,
    ValveState,
    CollisionStatus,
)
from .geometry import (
    expand_obstacle,
    expand_obstacles_with_global_clearance,
    point_in_any_obstacle,
    min_clearance_to_obstacles,
    estimate_safe_corridor,
    find_highest_obstacle_z,
)
from .collision import check_trajectory_collisions
from .velocity import apply_velocity_profile, get_non_swabbing_speed
from .valve_timing import apply_valve_timing


def generate_trajectory(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    robot_params: RobotParameters,
    swabbing_params: SwabbingParameters,
) -> TrajectoryResult:
    """
    Generate the complete swabbing trajectory.

    This is the main entry point for trajectory generation.
    It creates the trajectory points, applies velocity modulation,
    applies valve timing, and checks for collisions.

    If the direct centerline path is blocked, it tries an X offset
    within allowable limits.

    Args:
        mould: Mould geometry
        obstacles: List of obstacle envelopes
        robot_params: Robot and lance parameters
        swabbing_params: Swabbing process parameters

    Returns:
        TrajectoryResult with all points, collision status, and warnings.
    """
    # Set default swabbing parameters if not configured
    if swabbing_params.reference_diameter_mm <= 0:
        swabbing_params.reference_diameter_mm = mould.mould_diameter_mm
    if swabbing_params.coating_start_z_mm == 0:
        swabbing_params.coating_start_z_mm = mould.mould_top_z_mm
    if swabbing_params.coating_end_z_mm == 0:
        swabbing_params.coating_end_z_mm = mould.mould_bottom_z_mm

    global_clearance = robot_params.minimum_clearance_mm

    # Find the safe approach height and X position
    highest_obstacle_z = find_highest_obstacle_z(obstacles, global_clearance)
    approach_z = highest_obstacle_z + swabbing_params.approach_height_mm

    # Estimate safe corridor
    safe_corridor = estimate_safe_corridor(
        mould, obstacles, global_clearance,
        x_search_range_mm=robot_params.lance_length_mm * 0.8,
    )

    # Determine the swabbing X position
    swab_x = mould.mould_center_x_mm + swabbing_params.entry_offset_x_mm

    if safe_corridor is not None:
        # Ensure swab_x is within the safe corridor
        corridor_x_min, corridor_x_max = safe_corridor
        if swab_x < corridor_x_min or swab_x > corridor_x_max:
            # Clamp to safe corridor, preferring centre
            if mould.mould_center_x_mm >= corridor_x_min and \
               mould.mould_center_x_mm <= corridor_x_max:
                swab_x = mould.mould_center_x_mm
            else:
                # Use the corridor centre
                swab_x = (corridor_x_min + corridor_x_max) / 2.0

    # Generate raw trajectory points
    points = _build_trajectory_points(
        mould=mould,
        robot_params=robot_params,
        swabbing_params=swabbing_params,
        approach_z=approach_z,
        swab_x=swab_x,
    )

    # Apply velocity modulation
    points = apply_velocity_profile(
        points, robot_params,
        swabbing_params.reference_diameter_mm,
        mould.mould_diameter_mm,
    )

    # Apply valve timing
    points = apply_valve_timing(points, robot_params, swabbing_params)

    # Check collisions
    points, warnings = check_trajectory_collisions(
        points, obstacles, global_clearance,
    )

    # Determine feasibility
    has_collision = any(
        p.collision_status == CollisionStatus.COLLISION for p in points
    )

    feasible = not has_collision

    # If not feasible, try with X offset
    if not feasible:
        offset_result = _try_offset_trajectory(
            mould, obstacles, robot_params, swabbing_params,
            approach_z, swabbing_params,
        )
        if offset_result is not None:
            points, warnings_offset, feasible = offset_result
            warnings.extend(warnings_offset)
            if not feasible:
                warnings.append(
                    "WARNING: No feasible path found even with X offset. "
                    "Review obstacle geometry and clearance parameters."
                )

    return TrajectoryResult(
        points=points,
        collision_warnings=warnings,
        feasible=feasible,
    )


def _build_trajectory_points(
    mould: MouldGeometry,
    robot_params: RobotParameters,
    swabbing_params: SwabbingParameters,
    approach_z: float,
    swab_x: float,
) -> List[TrajectoryPoint]:
    """
    Build the raw trajectory point list.

    The trajectory structure:
      - Wait position (high, safe)
      - Approach points (descending toward mould)
      - Entry point (just above mould top, inside safe corridor)
      - Swab down points (inside mould, step by step)
      - Swab up points (optional, if include_swab_up=True)
      - Exit point (pulling out)
      - Return to wait

    Args:
        mould: Mould geometry
        robot_params: Robot parameters
        swabbing_params: Swabbing parameters
        approach_z: Z height for safe approach
        swab_x: X position for swabbing (along mould center or offset)

    Returns:
        List of TrajectoryPoint objects.
    """
    points = []
    pid = 0

    # The nozzle X position = swab_x (centre or offset)
    # The robot TCP is at the top of the lance
    # For a vertical lance: robot_x = nozzle_x, robot_z = nozzle_z + lance_length

    # === 1. WAIT POSITION ===
    wait_x = swab_x
    wait_z = approach_z
    points.append(TrajectoryPoint(
        point_id=pid, x_mm=wait_x, z_mm=wait_z,
        speed_mm_s=0.0, valve_state=ValveState.OFF,
        segment_type=SegmentType.WAIT,
        note="Wait position — safe height above obstacles",
    ))
    pid += 1

    # === 2. APPROACH ===
    # Move down from wait height to just above the mould top
    # Adding several intermediate approach points for smooth motion
    approach_target_z = mould.mould_top_z_mm + robot_params.minimum_clearance_mm + 10.0
    num_approach_steps = max(2, int((wait_z - approach_target_z) / 50.0))

    for i in range(1, num_approach_steps + 1):
        t = i / num_approach_steps
        az = wait_z + t * (approach_target_z - wait_z)
        points.append(TrajectoryPoint(
            point_id=pid, x_mm=swab_x, z_mm=az,
            speed_mm_s=0.0,  # Will be set by velocity module
            valve_state=ValveState.OFF,
            segment_type=SegmentType.APPROACH,
            note=f"Approach step {i}/{num_approach_steps}",
        ))
        pid += 1

    # === 3. ENTRY ===
    # Move horizontally or diagonally into the mould entry
    entry_z = mould.mould_top_z_mm
    points.append(TrajectoryPoint(
        point_id=pid, x_mm=swab_x, z_mm=entry_z,
        speed_mm_s=0.0,
        valve_state=ValveState.OFF,
        segment_type=SegmentType.ENTER,
        note="Entry — top of mould cavity",
    ))
    pid += 1

    # === 4. SWAB DOWN ===
    # Descend inside the mould from top to bottom
    coating_start = swabbing_params.coating_start_z_mm
    coating_end = swabbing_params.coating_end_z_mm
    step = swabbing_params.swab_step_mm

    # Ensure we swab from top to bottom of the mould
    swab_start_z = min(coating_start, mould.mould_top_z_mm)
    swab_end_z = max(coating_end, mould.mould_bottom_z_mm)

    current_z = swab_start_z
    while current_z > swab_end_z:
        next_z = max(current_z - step, swab_end_z)
        points.append(TrajectoryPoint(
            point_id=pid, x_mm=swab_x, z_mm=current_z,
            speed_mm_s=0.0,  # Set by velocity module
            valve_state=ValveState.OFF,  # Set by valve timing
            segment_type=SegmentType.SWAB_DOWN,
            note=f"Swab down Z={current_z:.1f}",
        ))
        pid += 1
        current_z = next_z

    # Final point at bottom of mould
    points.append(TrajectoryPoint(
        point_id=pid, x_mm=swab_x, z_mm=swab_end_z,
        speed_mm_s=0.0,
        valve_state=ValveState.OFF,
        segment_type=SegmentType.SWAB_DOWN,
        note=f"Swab down — bottom Z={swab_end_z:.1f}",
    ))
    pid += 1

    # === 5. SWAB UP (optional) ===
    if swabbing_params.include_swab_up:
        current_z = swab_end_z
        while current_z < swab_start_z:
            next_z = min(current_z + step, swab_start_z)
            points.append(TrajectoryPoint(
                point_id=pid, x_mm=swab_x, z_mm=max(current_z, swab_end_z),
                speed_mm_s=0.0,
                valve_state=ValveState.OFF,
                segment_type=SegmentType.SWAB_UP,
                note=f"Swab up Z={current_z:.1f}",
            ))
            pid += 1
            current_z = next_z

        # Final up point
        points.append(TrajectoryPoint(
            point_id=pid, x_mm=swab_x, z_mm=swab_start_z,
            speed_mm_s=0.0,
            valve_state=ValveState.OFF,
            segment_type=SegmentType.SWAB_UP,
            note="Swab up — top of mould",
        ))
        pid += 1

    # === 6. EXIT ===
    exit_z = mould.mould_top_z_mm + robot_params.minimum_clearance_mm + 5.0
    points.append(TrajectoryPoint(
        point_id=pid, x_mm=swab_x, z_mm=exit_z,
        speed_mm_s=0.0,
        valve_state=ValveState.OFF,
        segment_type=SegmentType.EXIT,
        note="Exit — above mould top with clearance",
    ))
    pid += 1

    # === 7. RETURN TO WAIT ===
    points.append(TrajectoryPoint(
        point_id=pid, x_mm=wait_x, z_mm=wait_z,
        speed_mm_s=0.0,
        valve_state=ValveState.OFF,
        segment_type=SegmentType.EXIT,
        note="Return to wait position",
    ))
    pid += 1

    return points


def _try_offset_trajectory(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    robot_params: RobotParameters,
    swabbing_params: SwabbingParameters,
    approach_z: float,
    original_swabbing_params: SwabbingParameters,
) -> Optional[Tuple[List[TrajectoryPoint], List[str], bool]]:
    """
    Try to find a feasible trajectory by offsetting the X position.

    Searches in steps from the mould centerline outward
    to find an X position where no collisions occur.

    Args:
        mould: Mould geometry
        obstacles: List of obstacles
        robot_params: Robot parameters
        swabbing_params: Swabbing parameters (will be modified for offset)
        approach_z: Safe approach Z height
        original_swabbing_params: Original swabbing params for reference

    Returns:
        (points, warnings, feasible) if feasible path found, None if not.
    """
    global_clearance = robot_params.minimum_clearance_mm
    max_offset = robot_params.lance_length_mm * 0.3
    offset_step = 5.0

    for offset in np.arange(offset_step, max_offset + offset_step, offset_step):
        for direction in [1, -1]:  # Try positive X then negative X
            test_x = mould.mould_center_x_mm + direction * offset

            # Build trajectory with offset
            modified_params = SwabbingParameters(
                reference_diameter_mm=swabbing_params.reference_diameter_mm,
                coating_start_z_mm=swabbing_params.coating_start_z_mm,
                coating_end_z_mm=swabbing_params.coating_end_z_mm,
                swab_step_mm=swabbing_params.swab_step_mm,
                include_swab_up=swabbing_params.include_swab_up,
                entry_offset_x_mm=direction * offset,
                approach_height_mm=swabbing_params.approach_height_mm,
            )

            points = _build_trajectory_points(
                mould, robot_params, modified_params,
                approach_z, test_x,
            )

            points = apply_velocity_profile(
                points, robot_params,
                swabbing_params.reference_diameter_mm,
                mould.mould_diameter_mm,
            )
            points = apply_valve_timing(points, robot_params, swabbing_params)

            points, warnings = check_trajectory_collisions(
                points, obstacles, global_clearance,
            )

            has_collision = any(
                p.collision_status == CollisionStatus.COLLISION for p in points
            )

            if not has_collision:
                warnings.append(
                    f"Feasible path found with X offset = "
                    f"{direction * offset:.1f} mm from centerline"
                )
                return points, warnings, True

    return None
