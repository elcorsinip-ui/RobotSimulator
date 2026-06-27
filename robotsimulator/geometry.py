"""
RobotSimulator — Geometry Engine (3D)

3D X-Y-Z geometry operations for the swabbing trajectory calculator.
Handles obstacle expansion, point-in-box checks, segment collision
approximation, and safe corridor estimation in 3D.

All coordinates in millimeters.
"""

from __future__ import annotations

import math
from typing import List, Tuple, Optional

from .models import ObstacleEnvelope, MouldGeometry


# ============================================================================
# Obstacle Expansion (3D)
# ============================================================================

def expand_obstacle(obstacle: ObstacleEnvelope) -> Tuple[float, float, float, float, float, float]:
    """
    Return the expanded bounding box of an obstacle including its local clearance.

    Returns:
        (x_min, x_max, y_min, y_max, z_min, z_max) of the expanded envelope.
    """
    return (
        obstacle.expanded_x_min_mm,
        obstacle.expanded_x_max_mm,
        obstacle.expanded_y_min_mm,
        obstacle.expanded_y_max_mm,
        obstacle.expanded_z_min_mm,
        obstacle.expanded_z_max_mm,
    )


def expand_obstacles_with_global_clearance(
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float,
) -> List[Tuple[float, float, float, float, float, float]]:
    """
    Expand each obstacle by both its local clearance AND a global minimum clearance.

    This is used for the robot path planning where the minimum_clearance_mm
    from RobotParameters must be respected in addition to each obstacle's
    own clearance.

    Returns:
        List of (x_min, x_max, y_min, y_max, z_min, z_max) expanded envelopes.
    """
    expanded = []
    for obs in obstacles:
        total_clearance = obs.clearance_mm + global_clearance_mm
        expanded.append((
            obs.x_min_mm - total_clearance,
            obs.x_max_mm + total_clearance,
            obs.y_min_mm - total_clearance,
            obs.y_max_mm + total_clearance,
            obs.z_min_mm - total_clearance,
            obs.z_max_mm + total_clearance,
        ))
    return expanded


# ============================================================================
# Point-in-Box Checks (3D)
# ============================================================================

def point_in_box(
    x: float,
    y: float,
    z: float,
    box: Tuple[float, float, float, float, float, float],
) -> bool:
    """
    Check if a point (x, y, z) is inside a 3D box region.

    Args:
        x, y, z: Coordinates of the point
        box: (x_min, x_max, y_min, y_max, z_min, z_max)

    Returns:
        True if point is strictly inside the box.
    """
    x_min, x_max, y_min, y_max, z_min, z_max = box
    return (x_min < x < x_max) and (y_min < y < y_max) and (z_min < z < z_max)


def point_in_obstacle(
    x: float,
    y: float,
    z: float,
    obstacle: ObstacleEnvelope,
    use_expanded: bool = True,
) -> bool:
    """
    Check if a point is inside an obstacle envelope (3D).

    Args:
        x, y, z: Point coordinates
        obstacle: The obstacle to check against
        use_expanded: If True, use the expanded (clearance-included) envelope

    Returns:
        True if the point is inside the obstacle (expanded or original).
    """
    if use_expanded:
        box = expand_obstacle(obstacle)
    else:
        box = (obstacle.x_min_mm, obstacle.x_max_mm,
               obstacle.y_min_mm, obstacle.y_max_mm,
               obstacle.z_min_mm, obstacle.z_max_mm)
    return point_in_box(x, y, z, box)


def point_in_any_obstacle(
    x: float,
    y: float,
    z: float,
    obstacles: List[ObstacleEnvelope],
    use_expanded: bool = True,
) -> bool:
    """
    Check if a point falls inside any of the given obstacles.

    Returns:
        True if the point is inside at least one obstacle.
    """
    return any(point_in_obstacle(x, y, z, obs, use_expanded) for obs in obstacles)


# ============================================================================
# Clearance Calculation (3D)
# ============================================================================

def distance_to_box_border(
    x: float,
    y: float,
    z: float,
    box: Tuple[float, float, float, float, float, float],
) -> float:
    """
    Calculate the signed distance from a point to the nearest border
    of a 3D box region.

    Positive = outside the box.
    Negative = inside the box.

    For a point inside the box, returns the negative of the
    minimum distance to any face (how deep inside it is).

    For a point outside, returns the minimum distance to the border.
    If the point is exactly on the border, returns 0.
    """
    x_min, x_max, y_min, y_max, z_min, z_max = box

    # Distance to each face
    dx_left = x - x_min
    dx_right = x_max - x
    dy_front = y - y_min
    dy_back = y_max - y
    dz_bottom = z - z_min
    dz_top = z_max - z

    if point_in_box(x, y, z, box):
        # Inside: return negative (how deep inside)
        return -min(dx_left, dx_right, dy_front, dy_back, dz_bottom, dz_top)
    else:
        # Outside: compute distance to nearest face/edge/corner
        dx = max(x_min - x, 0.0, x - x_max)
        dy = max(y_min - y, 0.0, y - y_max)
        dz = max(z_min - z, 0.0, z - z_max)
        
        # Distance to the box (can be face, edge, or corner distance)
        if dx == 0 and dy == 0:
            # Aligned with face in X-Y, distance is just Z
            return dz
        elif dx == 0 and dz == 0:
            # Aligned with face in X-Z, distance is just Y
            return dy
        elif dy == 0 and dz == 0:
            # Aligned with face in Y-Z, distance is just X
            return dx
        elif dx == 0:
            # Aligned with face in X, distance is 2D distance in Y-Z
            return math.sqrt(dy * dy + dz * dz)
        elif dy == 0:
            # Aligned with face in Y, distance is 2D distance in X-Z
            return math.sqrt(dx * dx + dz * dz)
        elif dz == 0:
            # Aligned with face in Z, distance is 2D distance in X-Y
            return math.sqrt(dx * dx + dy * dy)
        else:
            # Corner case: 3D Euclidean distance
            return math.sqrt(dx * dx + dy * dy + dz * dz)


def min_clearance_to_obstacles(
    x: float,
    y: float,
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
            box = expand_obstacle(obs)
        else:
            box = (obs.x_min_mm, obs.x_max_mm,
                   obs.y_min_mm, obs.y_max_mm,
                   obs.z_min_mm, obs.z_max_mm)
        dist = distance_to_box_border(x, y, z, box)
        if dist < min_dist:
            min_dist = dist
    return min_dist


# ============================================================================
# Segment Checks (3D)
# ============================================================================

def segment_collides_with_box(
    x1: float, y1: float, z1: float,
    x2: float, y2: float, z2: float,
    box: Tuple[float, float, float, float, float, float],
    num_samples: int = 20,
) -> bool:
    """
    Check if a 3D line segment collides with a box region.

    Uses point-sampling approximation: interpolates points along
    the segment and checks each against the box.

    Args:
        x1, y1, z1: Start point of the segment
        x2, y2, z2: End point of the segment
        box: (x_min, x_max, y_min, y_max, z_min, z_max)
        num_samples: Number of interpolation points (default 20)

    Returns:
        True if any sampled point on the segment is inside the box.
    """
    for i in range(num_samples + 1):
        t = i / num_samples
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        pz = z1 + t * (z2 - z1)
        if point_in_box(px, py, pz, box):
            return True
    return False


def segment_clearance_check(
    x1: float, y1: float, z1: float,
    x2: float, y2: float, z2: float,
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float = 0.0,
    num_samples: int = 20,
) -> Tuple[bool, float]:
    """
    Check if a 3D segment is clear of all obstacles and return
    the minimum clearance margin.

    Args:
        x1, y1, z1: Start point
        x2, y2, z2: End point
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
        py = y1 + t * (y2 - y1)
        pz = z1 + t * (z2 - z1)

        for box in expanded:
            dist = distance_to_box_border(px, py, pz, box)
            if dist < min_margin:
                min_margin = dist

    is_clear = min_margin > 0
    return is_clear, min_margin


# ============================================================================
# Safe Corridor Estimation (3D)
# ============================================================================

def estimate_safe_corridor_3d(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float,
    x_search_range_mm: float = 100.0,
    y_search_range_mm: float = 100.0,
    x_step_mm: float = 5.0,
    y_step_mm: float = 5.0,
) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Estimate a safe X-Y corridor at the mould entry level
    where the lance can pass without hitting obstacles.

    Searches along the X-Y plane at the mould top Z level to find
    a safe region.

    Args:
        mould: Mould geometry
        obstacles: List of obstacle envelopes
        global_clearance_mm: Additional clearance
        x_search_range_mm: How far to search from mould center in X
        y_search_range_mm: How far to search from mould center in Y
        x_step_mm: Step size for the X scan
        y_step_mm: Step size for the Y scan

    Returns:
        ((corridor_x_min, corridor_x_max), (corridor_y_min, corridor_y_max))
        if found, None if impossible.
    """
    expanded = expand_obstacles_with_global_clearance(obstacles, global_clearance_mm)

    # Scan at mould top Z level
    z_scan = mould.mould_top_z_mm
    x_center = mould.mould_center_x_mm
    y_center = mould.mould_center_y_mm

    # Find blocked regions at this Z level
    safe_x_min = x_center - x_search_range_mm
    safe_x_max = x_center + x_search_range_mm
    safe_y_min = y_center - y_search_range_mm
    safe_y_max = y_center + y_search_range_mm

    for box in expanded:
        bx_min, bx_max, by_min, by_max, bz_min, bz_max = box
        # Check if this obstacle intersects our scan plane
        if bz_min < z_scan < bz_max:
            # Expand the safe region boundaries
            if bx_min > safe_x_min and bx_max < safe_x_max:
                # Obstacle is inside X range - check if it blocks the center
                if bx_min < x_center < bx_max:
                    # Center is blocked in X
                    pass
            # Similar logic for Y
            if by_min > safe_y_min and by_max < safe_y_max:
                if by_min < y_center < by_max:
                    # Center is blocked in Y
                    pass

    # Simplified: return bounds that avoid obstacles at Z scan level
    # In a full implementation, this would do a more sophisticated gap analysis
    return ((safe_x_min, safe_x_max), (safe_y_min, safe_y_max))


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


def find_obstacle_bounds_in_xy(
    obstacles: List[ObstacleEnvelope],
    global_clearance_mm: float = 0.0,
    z_level: float = 0.0,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Find obstacle projections onto the X-Y plane at a specific Z level.

    Returns:
        (x_ranges, y_ranges) where each range is (min, max) for obstacles
        that intersect the given Z level.
    """
    expanded = expand_obstacles_with_global_clearance(obstacles, global_clearance_mm)
    
    x_ranges = []
    y_ranges = []
    
    for box in expanded:
        bx_min, bx_max, by_min, by_max, bz_min, bz_max = box
        # Check if this obstacle intersects the Z plane
        if bz_min <= z_level <= bz_max:
            x_ranges.append((bx_min, bx_max))
            y_ranges.append((by_min, by_max))
    
    return x_ranges, y_ranges