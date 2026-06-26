"""
RobotSimulator — Collision Detection

Collision checking for the X-Z swabbing trajectory.
Validates trajectory points and segments against obstacle envelopes.

All coordinates in millimeters.
"""

from __future__ import annotations

import math
from typing import List, Tuple

from .models import (
    ObstacleEnvelope,
    TrajectoryPoint,
    TrajectoryResult,
    CollisionStatus,
)
from .geometry import (
    expand_obstacle,
    expand_obstacles_with_global_clearance,
    point_in_any_obstacle,
    min_clearance_to_obstacles,
    distance_to_rect_border,
    segment_collides_with_rect,
    segment_clearance_check,
)


# ============================================================================
# Warning threshold
# ============================================================================

# Points within 1.5x the minimum clearance are flagged as "warning"
WARNING_CLEARANCE_FACTOR = 1.5


# ============================================================================
# Point Collision Check
# ============================================================================

def check_point_collision(
    x: float,
    z: float,
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float,
    warning_factor: float = WARNING_CLEARANCE_FACTOR,
) -> Tuple[CollisionStatus, float]:
    """
    Check a single point against all expanded obstacles.

    Args:
        x, z: Point coordinates
        obstacles: List of obstacle envelopes
        global_clearance_mm: Global minimum clearance
        warning_factor: Factor of clearance for warning zone

    Returns:
        (collision_status, clearance_margin_mm)
    """
    if not obstacles:
        return CollisionStatus.CLEAR, float("inf")

    expanded = expand_obstacles_with_global_clearance(obstacles, global_clearance_mm)

    # Check if point is inside any expanded obstacle
    for rect in expanded:
        # Use strict inside check (distance < 0 means inside)
        dist = distance_to_rect_border(x, z, rect)
        if dist < 0:
            # Point is inside an obstacle
            return CollisionStatus.COLLISION, dist

    # No collision — check for warning zone
    min_margin = float("inf")
    for rect in expanded:
        dist = distance_to_rect_border(x, z, rect)
        if dist < min_margin:
            min_margin = dist

    if min_margin < global_clearance_mm * warning_factor:
        return CollisionStatus.WARNING, min_margin

    return CollisionStatus.CLEAR, min_margin


# ============================================================================
# Trajectory Collision Check
# ============================================================================

def check_trajectory_collisions(
    points: List[TrajectoryPoint],
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float,
    num_segment_samples: int = 20,
) -> Tuple[List[TrajectoryPoint], List[str]]:
    """
    Check all trajectory points and segments for collisions.

    Updates the collision_status and clearance_margin_mm of each point.
    Also checks line segments between consecutive points.

    Args:
        points: List of trajectory points (will be modified in-place)
        obstacles: List of obstacle envelopes
        global_clearance_mm: Global minimum clearance
        num_segment_samples: Samples per segment for segment check

    Returns:
        (updated_points, warnings) where warnings is a list of
        descriptive warning messages.
    """
    warnings = []

    if not obstacles:
        for p in points:
            p.collision_status = CollisionStatus.CLEAR
            p.clearance_margin_mm = float("inf")
        return points, warnings

    # Check each point
    for point in points:
        status, margin = check_point_collision(
            point.x_mm, point.z_mm,
            obstacles, global_clearance_mm,
        )
        point.collision_status = status
        point.clearance_margin_mm = margin

        if status == CollisionStatus.COLLISION:
            warnings.append(
                f"Point {point.point_id} ({point.x_mm:.1f}, {point.z_mm:.1f}) "
                f"COLLISION — inside obstacle (margin: {margin:.1f} mm)"
            )
        elif status == CollisionStatus.WARNING:
            warnings.append(
                f"Point {point.point_id} ({point.x_mm:.1f}, {point.z_mm:.1f}) "
                f"WARNING — close to obstacle (margin: {margin:.1f} mm)"
            )

    # Check segments between consecutive points
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        is_clear, seg_margin = segment_clearance_check(
            p1.x_mm, p1.z_mm,
            p2.x_mm, p2.z_mm,
            obstacles, global_clearance_mm,
            num_samples=num_segment_samples,
        )

        if not is_clear:
            # Mark both points as having a segment collision issue
            if p1.collision_status == CollisionStatus.CLEAR:
                p1.collision_status = CollisionStatus.WARNING
                p1.clearance_margin_mm = min(p1.clearance_margin_mm, seg_margin)
                warnings.append(
                    f"Segment {p1.point_id}->{p2.point_id} passes through "
                    f"obstacle zone (margin: {seg_margin:.1f} mm)"
                )
            if p2.collision_status == CollisionStatus.CLEAR:
                p2.collision_status = CollisionStatus.WARNING
                p2.clearance_margin_mm = min(p2.clearance_margin_mm, seg_margin)

    return points, warnings
