"""
RobotSimulator — Valve Timing

Calculates valve ON/OFF timing for the swabbing trajectory.
Accounts for valve opening/closing delay to ensure coating
starts and stops at the correct positions.

First-order simplified model:
    valve_advance_distance_mm = speed_mm_s * valve_delay_ms / 1000

Conservative approach:
    Valve ON  = coating_start_z - valve_advance_distance
    Valve OFF = coating_end_z

All dimensions in millimeters.
"""

from __future__ import annotations

from typing import List

from .models import (
    RobotParameters,
    SwabbingParameters,
    TrajectoryPoint,
    ValveState,
    SegmentType,
)


def calculate_valve_advance_distance(
    speed_mm_s: float,
    valve_delay_ms: float,
) -> float:
    """
    Calculate the distance the robot travels during the valve delay.

    This is the distance the robot covers from the moment the valve
    command is sent to the moment the valve actually opens/closes.

    Args:
        speed_mm_s: Robot speed at the valve command position
        valve_delay_ms: Valve opening/closing delay in milliseconds

    Returns:
        Advance distance in mm (always >= 0).
    """
    if speed_mm_s <= 0 or valve_delay_ms < 0:
        return 0.0
    return speed_mm_s * valve_delay_ms / 1000.0


def calculate_valve_on_position(
    coating_start_z_mm: float,
    speed_mm_s: float,
    valve_delay_ms: float,
    approach_direction: str = "from_above",
) -> float:
    """
    Calculate the Z position where the valve ON command should be issued.

    If the robot approaches from above (swab_down), the valve must
    open BEFORE reaching the coating start, so the ON command is
    issued at a higher Z.

    Args:
        coating_start_z_mm: Z coordinate where coating should start
        speed_mm_s: Robot speed at the valve command position
        valve_delay_ms: Valve opening delay in ms
        approach_direction: "from_above" (swab_down) or "from_below" (swab_up)

    Returns:
        Z coordinate where valve ON command should be issued.
    """
    advance = calculate_valve_advance_distance(speed_mm_s, valve_delay_ms)
    if approach_direction == "from_above":
        # Robot moves downward: open valve above coating start
        return coating_start_z_mm + advance
    else:
        # Robot moves upward: open valve below coating start
        return coating_start_z_mm - advance


def calculate_valve_off_position(
    coating_end_z_mm: float,
    speed_mm_s: float,
    valve_delay_ms: float,
    approach_direction: str = "from_above",
    compensate_closing: bool = False,
) -> float:
    """
    Calculate the Z position where the valve OFF command should be issued.

    Conservative model (default): valve closes AT the coating end position.
    Compensated model: valve closes BEFORE the coating end to account
    for closing delay.

    Args:
        coating_end_z_mm: Z coordinate where coating should stop
        speed_mm_s: Robot speed at the valve command position
        valve_delay_ms: Valve closing delay in ms
        approach_direction: "from_above" or "from_below"
        compensate_closing: If True, compensate for closing delay

    Returns:
        Z coordinate where valve OFF command should be issued.
    """
    if not compensate_closing:
        # Conservative: close at the end
        return coating_end_z_mm

    advance = calculate_valve_advance_distance(speed_mm_s, valve_delay_ms)
    if approach_direction == "from_above":
        # Robot moves downward: close valve before reaching end
        return coating_end_z_mm + advance
    else:
        # Robot moves upward: close valve after passing end
        return coating_end_z_mm - advance


def apply_valve_timing(
    points: List[TrajectoryPoint],
    robot_params: RobotParameters,
    swabbing_params: SwabbingParameters,
) -> List[TrajectoryPoint]:
    """
    Apply valve ON/OFF timing to a trajectory.

    Sets the valve_state for each trajectory point based on whether
    the point is inside the coating zone, accounting for valve delay
    compensation.

    Logic:
        - Valve ON starts before coating zone (by advance distance)
        - Valve OFF at or before coating zone end
        - All non-swabbing segments: valve OFF

    Args:
        points: List of trajectory points (will be modified in-place)
        robot_params: Robot parameters (valve_delay_ms, speeds)
        swabbing_params: Swabbing parameters (coating start/end Z)

    Returns:
        Modified list with updated valve_state and notes.
    """
    coating_start_z = swabbing_params.coating_start_z_mm
    coating_end_z = swabbing_params.coating_end_z_mm

    # Get the swabbing speed for advance calculation
    swab_points = [p for p in points if p.segment_type in
                   (SegmentType.SWAB_DOWN, SegmentType.SWAB_UP)]

    if swab_points:
        # Use average swabbing speed for advance calculation
        avg_swab_speed = sum(p.speed_mm_s for p in swab_points) / len(swab_points)
    else:
        avg_swab_speed = robot_params.nominal_speed_mm_s

    # Determine approach direction
    has_swab_down = any(p.segment_type == SegmentType.SWAB_DOWN for p in points)
    has_swab_up = any(p.segment_type == SegmentType.SWAB_UP for p in points)

    approach_dir = "from_above" if has_swab_down else "from_below"

    # Calculate valve ON/OFF Z positions
    valve_on_z = calculate_valve_on_position(
        coating_start_z, avg_swab_speed,
        robot_params.valve_delay_ms, approach_dir,
    )
    valve_off_z = calculate_valve_off_position(
        coating_end_z, avg_swab_speed,
        robot_params.valve_delay_ms, approach_dir,
        compensate_closing=False,
    )

    advance_dist = calculate_valve_advance_distance(
        avg_swab_speed, robot_params.valve_delay_ms,
    )

    # Apply valve state to each point
    for point in points:
        if point.segment_type in (SegmentType.WAIT, SegmentType.APPROACH,
                                   SegmentType.ENTER, SegmentType.EXIT):
            point.valve_state = ValveState.OFF
            continue

        # Swabbing segments
        if approach_dir == "from_above":
            # Robot moves downward: Z decreases
            # Valve ON when Z <= valve_on_z (above coating start + advance)
            # Valve OFF when Z <= valve_off_z (at coating end, i.e. lowest point)
            if point.z_mm <= valve_on_z and point.z_mm >= valve_off_z:
                point.valve_state = ValveState.ON
            elif point.z_mm > valve_on_z and advance_dist > 0:
                # Approaching coating zone: turn ON early
                point.valve_state = ValveState.ON
                point.note = (point.note + " [Valve advance ON]" if point.note
                              else "Valve advance ON")
            else:
                point.valve_state = ValveState.OFF
        else:
            # Robot moves upward: Z increases
            if point.z_mm >= valve_on_z and point.z_mm <= valve_off_z:
                point.valve_state = ValveState.ON
            else:
                point.valve_state = ValveState.OFF

    # Add note to first ON point about advance
    for point in points:
        if point.valve_state == ValveState.ON:
            point.note = (point.note + f" | Advance: {advance_dist:.1f}mm"
                          if point.note
                          else f"Valve advance: {advance_dist:.1f}mm")
            break

    return points
