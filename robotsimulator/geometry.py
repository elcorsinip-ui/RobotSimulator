"""
RobotSimulator — Geometry Engine

2D X-Z geometry operations for the swabbing trajectory calculator.
Handles obstacle expansion, point-in-obstacle checks, segment
collision approximation, and safe corridor estimation.

All coordinates in millimeters.
"""

from __future__ import annotations

import math
from typing import List, Tuple, Optional

from .models import ObstacleEnvelope, MouldGeometry


# ============================================================================
# Obstacle Expansion
# ============================================================================

def expand_obstacle(obstacle: ObstacleEnvelope) -> Tuple[float, float, float, float]:
    """
    Return the expanded bounding box of an obstacle including its local clearance.

    Returns:
        (x_min, x_max, z_min, z_max) of the expanded envelope.
    """
    return (
        obstacle.expanded_x_min_mm,
        obstacle.expanded_x_max_mm,
        obstacle.expanded_z_min_mm,
        obstacle.expanded_z_max_mm,
    )


def expand_obstacles_with_global_clearance(
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float,
) -> List[Tuple[float, float, float, float]]:
    """
    Expand each obstacle by both its local clearance AND a global minimum clearance.

    This is used for the robot path planning where the minimum_clearance_mm
    from RobotParameters must be respected in addition to each obstacle's
    own clearance.

    Returns:
        List of (x_min, x_max, z_min, z_max) expanded envelopes.
    """
    expanded = []
    for obs in obstacles:
        total_clearance = obs.clearance_mm + global_clearance_mm
        expanded.append((
            obs.x_min_mm - total_clearance,
            obs.x_max_mm + total_clearance,
            obs.z_min_mm - total_clearance,
            obs.z_max_mm + total_clearance,
        ))
    return expanded


# ============================================================================
# Point-in-Obstacle Checks
# ============================================================================

def point_in_rect(
    x: float,
    z: float,
    rect: Tuple[float, float, float, float],
) -> bool:
    """
    Check if a point (x, z) is inside a rectangular region.

    Args:
        x: X coordinate of the point
        z: Z coordinate of the point
        rect: (x_min, x_max, z_min, z_max)

    Returns:
        True if point is strictly inside the rectangle.
    """
    x_min, x_max, z_min, z_max = rect
    return (x_min < x < x_max) and (z_min < z < z_max)


def point_in_obstacle(
    x: float,
    z: float,
    obstacle: ObstacleEnvelope,
    use_expanded: bool = True,
) -> bool:
    """
    Check if a point is inside an obstacle envelope.

    Args:
        x, z: Point coordinates
        obstacle: The obstacle to check against
        use_expanded: If True, use the expanded (clearance-included) envelope

    Returns:
        True if the point is inside the obstacle (expanded or original).
    """
    if use_expanded:
        rect = expand_obstacle(obstacle)
    else:
        rect = (obstacle.x_min_mm, obstacle.x_max_mm,
                obstacle.z_min_mm, obstacle.z_max_mm)
    return point_in_rect(x, z, rect)


def point_in_any_obstacle(
    x: float,
    z: float,
    obstacles: List[ObstacleEnvelope],
    use_expanded: bool = True,
) -> bool:
    """
    Check if a point falls inside any of the given obstacles.

    Returns:
        True if the point is inside at least one obstacle.
    """
    return any(point_in_obstacle(x, z, obs, use_expanded) for obs in obstacles)


# ============================================================================
# Clearance Calculation
# ============================================================================

def distance_to_rect_border(
    x: float,
    z: float,
    rect: Tuple[float, float, float, float],
) -> float:
    """
    Calculate the signed distance from a point to the nearest border
    of a rectangular region.

    Positive = outside the rectangle.
    Negative = inside the rectangle.

    For a point inside the rectangle, returns the negative of the
    minimum distance to any border (how deep inside it is).

    For a point outside, returns the minimum distance to the border.
    If the point is exactly on the border, returns 0.
    """
    x_min, x_max, z_min, z_max = rect

    # Distance to each border
    dx_left = x - x_min
    dx_right = x_max - x
    dz_bottom = z - z_min
    dz_top = z_max - z

    if point_in_rect(x, z, rect):
        # Inside: return negative (how deep inside)
        return -min(dx_left, dx_right, dz_bottom, dz_top)
    else:
        # Outside: compute distance to nearest edge or corner
        dx = max(x_min - x, 0.0, x - x_max)
        dz = max(z_min - z, 0.0, z - z_max)
        return math.sqrt(dx * dx + dz * dz)


def min_clearance_to_obstacles(
    x: float,
    z: float,
    obstacles: List[ObstacleEnvelope],
    use_expanded: bool = True,
) -> float:
    """
    Calculate the minimum clearance from a point to the nearest
    obstacle border (using expanded or original envelopes).

    Returns:
        Distance to the nearest obstacle border.
        Positive = clear, 0 = on border, negative = inside obstacle.
        If no obstacles, returns float('inf').
    """
    if not obstacles:
        return float("inf")

    min_dist = float("inf")
    for obs in obstacles:
        if use_expanded:
            rect = expand_obstacle(obs)
        else:
            rect = (obs.x_min_mm, obs.x_max_mm,
                    obs.z_min_mm, obs.z_max_mm)
        dist = distance_to_rect_border(x, z, rect)
        if dist < min_dist:
            min_dist = dist
    return min_dist


# ============================================================================
# Segment Checks
# ============================================================================

def segment_collides_with_rect(
    x1: float, z1: float,
    x2: float, z2: float,
    rect: Tuple[float, float, float, float],
    num_samples: int = 20,
) -> bool:
    """
    Check if a line segment collides with a rectangular region.

    Uses point-sampling approximation: interpolates points along
    the segment and checks each against the rectangle.

    Args:
        x1, z1: Start point of the segment
        x2, z2: End point of the segment
        rect: (x_min, x_max, z_min, z_max)
        num_samples: Number of interpolation points (default 20)

    Returns:
        True if any sampled point on the segment is inside the rectangle.
    """
    for i in range(num_samples + 1):
        t = i / num_samples
        px = x1 + t * (x2 - x1)
        pz = z1 + t * (z2 - z1)
        if point_in_rect(px, pz, rect):
            return True
    return False


def segment_clearance_check(
    x1: float, z1: float,
    x2: float, z2: float,
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float = 0.0,
    num_samples: int = 20,
) -> Tuple[bool, float]:
    """
    Check if a segment is clear of all obstacles and return
    the minimum clearance margin.

    Args:
        x1, z1: Start point
        x2, z2: End point
        obstacles: List of obstacle envelopes
        global_clearance_mm: Additional global clearance to apply
        num_samples: Number of sample points along the segment

    Returns:
        (is_clear, min_margin):
            is_clear = True if no collision detected
            min_margin = minimum clearance to nearest obstacle
    """
    expanded = expand_obstacles_with_global_clearance(obstacles, global_clearance_mm)
    min_margin = float("inf")

    for i in range(num_samples + 1):
        t = i / num_samples
        px = x1 + t * (x2 - x1)
        pz = z1 + t * (z2 - z1)

        for rect in expanded:
            dist = distance_to_rect_border(px, pz, rect)
            if dist < min_margin:
                min_margin = dist

    is_clear = min_margin > 0
    return is_clear, min_margin


# ============================================================================
# Safe Corridor Estimation
# ============================================================================

def estimate_safe_corridor(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float,
    x_search_range_mm: float = 100.0,
    x_step_mm: float = 5.0,
) -> Optional[Tuple[float, float]]:
    """
    Estimate a safe X corridor (x_min, x_max) at the mould entry level
    where the lance can pass without hitting obstacles.

    Searches along the X axis at the mould top Z level to find
    the widest gap in the expanded obstacles.

    Args:
        mould: Mould geometry
        obstacles: List of obstacle envelopes
        global_clearance_mm: Additional clearance
        x_search_range_mm: How far to search from mould center
        x_step_mm: Step size for the X scan

    Returns:
        (corridor_x_min, corridor_x_max) if found, None if impossible.
    """
    expanded = expand_obstacles_with_global_clearance(obstacles, global_clearance_mm)

    # Scan at mould top Z level
    z_scan = mould.mould_top_z_mm
    x_center = mould.mould_center_x_mm
    x_start = x_center - x_search_range_mm
    x_end = x_center + x_search_range_mm

    # Build a list of blocked X positions
    blocked_ranges = []
    for rect in expanded:
        x_min_exp, x_max_exp, z_min_exp, z_max_exp = rect
        if z_min_exp < z_scan < z_max_exp:
            blocked_ranges.append((x_min_exp, x_max_exp))

    # Find the widest gap that includes the mould center
    # Sort blocked ranges by x_min
    blocked_ranges.sort(key=lambda r: r[0])

    # Find free intervals
    current_x = x_start
    free_intervals = []
    for bx_min, bx_max in blocked_ranges:
        if bx_min > current_x:
            free_intervals.append((current_x, bx_min))
        current_x = max(current_x, bx_max)
    if current_x < x_end:
        free_intervals.append((current_x, x_end))

    # Find the interval closest to mould center
    best_interval = None
    best_distance = float("inf")

    for fx_min, fx_max in free_intervals:
        if fx_min <= x_center <= fx_max:
            # Center is inside this interval — best case
            return (fx_min, fx_max)
        # Distance from interval to center
        if fx_max < x_center:
            dist = x_center - fx_max
        else:
            dist = fx_min - x_center
        if dist < best_distance:
            best_distance = dist
            best_interval = (fx_min, fx_max)

    return best_interval


def find_highest_obstacle_z(
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float = 0.0,
) -> float:
    """
    Find the highest Z coordinate of all expanded obstacles.

    Used to determine the approach height that clears all obstacles.

    Returns:
        Maximum Z coordinate across all expanded obstacle tops.
        Returns 0 if no obstacles.
    """
    if not obstacles:
        return 0.0

    max_z = float("-inf")
    for obs in obstacles:
        top_z = obs.z_max_mm + obs.clearance_mm + global_clearance_mm
        if top_z > max_z:
            max_z = top_z

    return max_z if max_z > float("-inf") else 0.0
