"""
RobotSimulator — Unit Tests for Collision Detection
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
            z_min_mm=210.0,
            z_max_mm=240.0,
            clearance_mm=5.0,
        ),
    ]


@pytest.fixture
def clear_points():
    # All points and segments must be CLEAR of the expanded obstacle zone.
    # Expansione deflettore (clearance 5+10=15): x[-95, 95], z[195, 255].
    # Strategia: x=-100 (fuori dall'espansione orizzontale), segmento verticale
    # che non tocca la zona Z ostacolo.
    return [
        TrajectoryPoint(point_id=0, x_mm=0, z_mm=280, speed_mm_s=200,
                        segment_type=SegmentType.WAIT),
        TrajectoryPoint(point_id=1, x_mm=-100, z_mm=280, speed_mm_s=200,
                        segment_type=SegmentType.APPROACH),
        TrajectoryPoint(point_id=2, x_mm=-100, z_mm=170, speed_mm_s=100,
                        segment_type=SegmentType.ENTER),
        TrajectoryPoint(point_id=3, x_mm=-100, z_mm=160, speed_mm_s=100,
                        segment_type=SegmentType.ENTER),
    ]


@pytest.fixture
def collision_points():
    return [
        TrajectoryPoint(point_id=0, x_mm=0, z_mm=220, speed_mm_s=100,
                        segment_type=SegmentType.SWAB_DOWN),
    ]


# ============================================================================
# Point Collision Tests
# ============================================================================

class TestCheckPointCollision:
    def test_clear_point(self, obstacles):
        status, margin = check_point_collision(0, 100, obstacles, 10.0)
        assert status == CollisionStatus.CLEAR
        assert margin > 0

    def test_collision_point(self, obstacles):
        # Point at (0, 220) — inside deflector (z 210-240)
        status, margin = check_point_collision(0, 220, obstacles, 10.0)
        # With global_clearance=10, expanded z range is 195-255
        assert status == CollisionStatus.COLLISION
        assert margin < 0

    def test_warning_point(self, obstacles):
        # Point just outside expanded zone
        # Deflector expanded with global=10: z 195-255
        # Point at z=257 is just outside but within warning range
        status, margin = check_point_collision(0, 257, obstacles, 10.0)
        # Should be clear (outside 255 + enough margin)
        assert status in (CollisionStatus.CLEAR, CollisionStatus.WARNING)

    def test_no_obstacles(self):
        status, margin = check_point_collision(0, 0, [], 10.0)
        assert status == CollisionStatus.CLEAR
        assert margin == float("inf")


# ============================================================================
# Trajectory Collision Tests
# ============================================================================

class TestCheckTrajectoryCollisions:
    def test_clear_trajectory(self, clear_points, obstacles):
        points, warnings = check_trajectory_collisions(
            clear_points, obstacles, 10.0,
        )
        assert all(p.collision_status == CollisionStatus.CLEAR for p in points)

    def test_collision_trajectory(self, collision_points, obstacles):
        points, warnings = check_trajectory_collisions(
            collision_points, obstacles, 10.0,
        )
        has_not_clear = any(
            p.collision_status != CollisionStatus.CLEAR for p in points
        )
        assert has_not_clear  # Should be COLLISION or WARNING
        assert len(warnings) > 0

    def test_no_obstacles(self, clear_points):
        points, warnings = check_trajectory_collisions(
            clear_points, [], 10.0,
        )
        assert all(p.collision_status == CollisionStatus.CLEAR for p in points)
        assert len(warnings) == 0

    def test_clearance_margin_populated(self, clear_points, obstacles):
        points, warnings = check_trajectory_collisions(
            clear_points, obstacles, 10.0,
        )
        for p in points:
            assert p.clearance_margin_mm != 0  # Should be set to something
