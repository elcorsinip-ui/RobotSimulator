"""
RobotSimulator — Velocity Modulation

Calculates robot speed at each trajectory point to achieve
approximately uniform coating thickness inside the mould.

First-order engineering model:
    relative_surface_factor = local_diameter_mm / reference_diameter_mm
    raw_speed = nominal_speed_mm_s / relative_surface_factor
    speed = clamp(raw_speed, min_robot_speed, max_robot_speed)

All dimensions in millimeters, speeds in mm/s.
"""

from __future__ import annotations

from typing import List

from .models import RobotParameters, SwabbingParameters, TrajectoryPoint, SegmentType


def calculate_velocity(
    local_diameter_mm: float,
    reference_diameter_mm: float,
    nominal_speed_mm_s: float,
    min_speed_mm_s: float,
    max_speed_mm_s: float,
) -> float:
    """
    Calculate the robot speed for a given local mould diameter.

    The principle: at larger diameter, the surface area is larger
    per unit height, so the robot must move slower to deposit
    the same amount of coating per unit area.

    Conversely, at smaller diameter the robot can move faster.

    Args:
        local_diameter_mm: Mould diameter at the current Z level
        reference_diameter_mm: Reference diameter (usually the mould's
            nominal diameter for calibration)
        nominal_speed_mm_s: Speed calibrated at the reference diameter
        min_speed_mm_s: Minimum allowed robot speed
        max_speed_mm_s: Maximum allowed robot speed

    Returns:
        Calculated speed clamped between min and max.

    Raises:
        ValueError: If reference_diameter_mm is zero or negative.
    """
    if reference_diameter_mm <= 0:
        raise ValueError(
            f"reference_diameter_mm must be > 0, got {reference_diameter_mm}"
        )

    relative_surface_factor = local_diameter_mm / reference_diameter_mm

    # Avoid division by zero if local diameter is zero
    if relative_surface_factor <= 0:
        return max_speed_mm_s

    raw_speed = nominal_speed_mm_s / relative_surface_factor
    speed = max(min_speed_mm_s, min(max_speed_mm_s, raw_speed))

    return speed


def get_swabbing_speed(
    robot_params: RobotParameters,
    reference_diameter_mm: float,
    local_diameter_mm: float = 0.0,
) -> float:
    """
    Convenience function: get the swabbing speed using RobotParameters.

    If local_diameter_mm is 0 or not specified, uses the reference diameter
    (which gives the nominal speed).

    Args:
        robot_params: Robot parameters containing speed limits
        reference_diameter_mm: Reference diameter for speed calibration
        local_diameter_mm: Local diameter at current Z level

    Returns:
        Calculated swabbing speed in mm/s.
    """
    if local_diameter_mm <= 0:
        local_diameter_mm = reference_diameter_mm

    return calculate_velocity(
        local_diameter_mm=local_diameter_mm,
        reference_diameter_mm=reference_diameter_mm,
        nominal_speed_mm_s=robot_params.nominal_speed_mm_s,
        min_speed_mm_s=robot_params.min_robot_speed_mm_s,
        max_speed_mm_s=robot_params.max_robot_speed_mm_s,
    )


def get_non_swabbing_speed(robot_params: RobotParameters) -> float:
    """
    Get the speed for non-swabbing segments (approach, enter, exit, wait).

    Uses nominal speed by default for these segments.
    Can be adjusted to max speed if desired.

    Args:
        robot_params: Robot parameters

    Returns:
        Nominal speed in mm/s.
    """
    return robot_params.nominal_speed_mm_s


def apply_velocity_profile(
    points: List[TrajectoryPoint],
    robot_params: RobotParameters,
    reference_diameter_mm: float,
    local_diameter_mm: float = 0.0,
) -> List[TrajectoryPoint]:
    """
    Apply velocity modulation to a list of trajectory points.

    Swabbing segments (swab_down, swab_up) get velocity-modulated speed.
    Non-swabbing segments (approach, enter, exit, wait) get nominal speed.

    Args:
        points: List of trajectory points to modify
        robot_params: Robot parameters
        reference_diameter_mm: Reference diameter for speed calibration
        local_diameter_mm: Local diameter (0 = use reference)

    Returns:
        The same list with updated speed_mm_s values.
    """
    swab_speed = get_swabbing_speed(robot_params, reference_diameter_mm, local_diameter_mm)
    transit_speed = get_non_swabbing_speed(robot_params)

    for point in points:
        if point.segment_type in (SegmentType.SWAB_DOWN, SegmentType.SWAB_UP):
            point.speed_mm_s = swab_speed
        else:
            point.speed_mm_s = transit_speed

    return points
