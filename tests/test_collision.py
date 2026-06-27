"""
RobotSimulator — Unit Tests for Collision Detection (3D)
"""

import pytest
from robotsimulator.models import (
    MouldGeometry,
    ObstacleEnvelope,
    ObstacleType,
    TrajectoryPoint,
    TrajectoryResult,
    CollisionStatus,
    ValveState,
    SegmentType,
)
from robotsimulator.collision import check_point_collision, check_trajectory_collisions


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def obstacles():
    return [
        ObstacleEnvelope(
            name="Deflector",
            obstacle_type=ObstacleType.DEFLECTOR,
            x_min_mm=-80.0,
            x_max_mm=80.0,
            y_min_mm=-50.0,
            y_max_mm=50.0,
            z_min_mm=210.0,
            z_max_mm=240.0,
            clearance_mm=5.0,
        ),
    ]


@pytest.fixture
def clear_points():
    """Points that are clear of the obstacle."""
    return [
        TrajectoryPoint(point_id=0, x_mm=0, y_mm=0, z_mm=280, speed_mm_s=200,
                        segment_type=SegmentType.WAIT),
        TrajectoryPoint(point_id=1, x_mm=-100, y_mm=0, z_mm=280, speed_mm_s=200,
                        segment_type=SegmentType.APPROACH),
        TrajectoryPoint(point_id=2, x_mm=-100, y_mm=0, z_mm=170, speed_mm_s=100,
                        segment_type=SegmentType.ENTER),
        TrajectoryPoint(point_id=3, x_mm=-100, y_mm=0, z_mm=160, speed_mm_s=100,
                        segment_type=SegmentType.ENTER),
    ]


@pytest.fixture
def collision_points():
    """Points inside the obstacle."""
    return [
        TrajectoryPoint(point_id=0, x_mm=0, y_mm=0, z_mm=220, speed_mm_s=100,
                        segment_type=SegmentType.SWAB_DOWN),
    ]


# ============================================================================
# Point Collision Tests (3D)
# ============================================================================

class TestCheckPointCollision:
    def test_clear_point(self, obstacles):
        status, margin = check_point_collision(0, 0, 100, obstacles, 10.0)
        assert status == CollisionStatus.CLEAR
        assert margin > 0

    def test_collision_point(self, obstacles):
        status, margin = check_point_collision(0, 0, 220, obstacles, 10.0)
        assert status == CollisionStatus.COLLISION
        assert margin < 0

    def test_collision_point_x_edge(self, obstacles):
        status, margin = check_point_collision(90, 0, 220, obstacles, 10.0)
        assert status == CollisionStatus.COLLISION

    def test_collision_point_y_edge(self, obstacles):
        status, margin = check_point_collision(0, 55, 220, obstacles, 10.0)
        assert status == CollisionStatus.COLLISION

    def test_warning_point(self, obstacles):
        status, margin = check_point_collision(0, 0, 257, obstacles, 10.0)
        assert status in (CollisionStatus.CLEAR, CollisionStatus.WARNING)

    def test_no_obstacles(self):
        status, margin = check_point_collision(0, 0, 0, [], 10.0)
        assert status == CollisionStatus.CLEAR
        assert margin == float("inf")


# ============================================================================
# Trajectory Collision Tests (3D)
# ============================================================================

class TestCheckTrajectoryCollisions:
    def test_clear_trajectory(self, clear_points, obstacles):
        points, warnings = check_trajectory_collisions(clear_points, obstacles, 10.0)
        assert all(p.collision_status == CollisionStatus.CLEAR for p in points)

    def test_collision_trajectory(self, collision_points, obstacles):
        points, warnings = check_trajectory_collisions(collision_points, obstacles, 10.0)
        has_not_clear = any(p.collision_status != CollisionStatus.CLEAR for p in points)
        assert has_not_clear
        assert len(warnings) > 0

    def test_no_obstacles(self, clear_points):
        points, warnings = check_trajectory_collisions(clear_points, [], 10.0)
        assert all(p.collision_status == CollisionStatus.CLEAR for p in points)
        assert len(warnings) == 0

    def test_clearance_margin_populated(self, clear_points, obstacles):
        points, warnings = check_trajectory_collisions(clear_points, obstacles, 10.0)
        for p in points:
            assert p.clearance_margin_mm != 0

    def test_3d_segment_collision(self, obstacles):
        """Test a segment that passes through obstacle in 3D."""
        points = [
            TrajectoryPoint(point_id=0, x_mm=0, y_mm=0, z_mm=300, speed_mm_s=200,
                            segment_type=SegmentType.APPROACH),
            TrajectoryPoint(point_id=1, x_mm=0, y_mm=0, z_mm=100, speed_mm_s=100,
                            segment_type=SegmentType.SWAB_DOWN),
        ]
        points, warnings = check_trajectory_collisions(points, obstacles, 10.0)
        has_not_clear = any(p.collision_status != CollisionStatus.CLEAR for p in points)
        assert has_not_clear