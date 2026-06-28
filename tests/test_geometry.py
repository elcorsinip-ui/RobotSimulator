"""
RobotSimulator — Unit Tests for Geometry Engine (3D)
"""

import pytest
from robotsimulator.models import MouldGeometry, ObstacleEnvelope, ObstacleType
from robotsimulator.geometry import (
    expand_obstacle,
    expand_obstacles_with_global_clearance,
    point_in_box,
    point_in_obstacle,
    point_in_any_obstacle,
    distance_to_box_border,
    min_clearance_to_obstacles,
    segment_collides_with_box,
    segment_clearance_check,
    estimate_safe_corridor_3d,
    find_highest_obstacle_z,
    find_obstacle_bounds_in_xy,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mould():
    return MouldGeometry(
        mould_diameter_mm=150.0,
        mould_height_mm=120.0,
        neck_height_mm=20.0,
        mould_top_z_mm=200.0,
        mould_center_x_mm=0.0,
        mould_center_y_mm=0.0,
        mould_depth_mm=0.0,
    )


@pytest.fixture
def mould_3d():
    """Mould with Y depth for 3D testing."""
    return MouldGeometry(
        mould_diameter_mm=150.0,
        mould_height_mm=120.0,
        neck_height_mm=20.0,
        mould_top_z_mm=200.0,
        mould_center_x_mm=0.0,
        mould_center_y_mm=0.0,
        mould_depth_mm=100.0,
    )


@pytest.fixture
def deflector():
    return ObstacleEnvelope(
        name="Test Deflector",
        obstacle_type=ObstacleType.DEFLECTOR,
        x_min_mm=-80.0,
        x_max_mm=80.0,
        y_min_mm=-50.0,
        y_max_mm=50.0,
        z_min_mm=210.0,
        z_max_mm=240.0,
        clearance_mm=5.0,
    )


@pytest.fixture
def baffle():
    return ObstacleEnvelope(
        name="Test Baffle",
        obstacle_type=ObstacleType.BAFFLE_MECHANISM,
        x_min_mm=-120.0,
        x_max_mm=-40.0,
        y_min_mm=-60.0,
        y_max_mm=0.0,
        z_min_mm=160.0,
        z_max_mm=260.0,
        clearance_mm=5.0,
    )


# ============================================================================
# Mould Geometry Tests (3D)
# ============================================================================

class TestMouldGeometry:
    def test_basic_creation(self, mould):
        assert mould.mould_diameter_mm == 150.0
        assert mould.mould_height_mm == 120.0
        assert mould.neck_height_mm == 20.0

    def test_3d_properties(self, mould_3d):
        assert mould_3d.mould_depth_mm == 100.0
        assert mould_3d.effective_y_depth_mm == 100.0
        assert mould_3d.mould_front_y_mm == -50.0
        assert mould_3d.mould_back_y_mm == 50.0

    def test_circular_mould(self, mould):
        # When depth=0, uses diameter
        assert mould.effective_y_depth_mm == 150.0

    def test_derived_properties(self, mould):
        assert mould.mould_bottom_z_mm == 80.0
        assert mould.neck_bottom_z_mm == 60.0
        assert mould.mould_left_x_mm == -75.0
        assert mould.mould_right_x_mm == 75.0
        assert mould.mould_radius_mm == 75.0

    def test_invalid_diameter(self):
        with pytest.raises(ValueError):
            MouldGeometry(mould_diameter_mm=-10, mould_height_mm=100)

    def test_invalid_height(self):
        with pytest.raises(ValueError):
            MouldGeometry(mould_diameter_mm=100, mould_height_mm=0)

    def test_negative_depth(self):
        with pytest.raises(ValueError):
            MouldGeometry(
                mould_diameter_mm=100, mould_height_mm=50,
                mould_depth_mm=-10,
            )


# ============================================================================
# Obstacle Envelope Tests (3D)
# ============================================================================

class TestObstacleEnvelope:
    def test_basic_creation(self, deflector):
        assert deflector.name == "Test Deflector"
        assert deflector.obstacle_type == ObstacleType.DEFLECTOR

    def test_expanded_envelope_3d(self, deflector):
        assert deflector.expanded_x_min_mm == -85.0
        assert deflector.expanded_x_max_mm == 85.0
        assert deflector.expanded_y_min_mm == -55.0
        assert deflector.expanded_y_max_mm == 55.0
        assert deflector.expanded_z_min_mm == 205.0
        assert deflector.expanded_z_max_mm == 245.0

    def test_center_and_dimensions(self, deflector):
        assert deflector.center_x_mm == 0.0
        assert deflector.center_y_mm == 0.0
        assert deflector.center_z_mm == 225.0
        assert deflector.width_mm == 160.0
        assert deflector.depth_mm == 100.0
        assert deflector.height_mm == 30.0

    def test_volume(self, deflector):
        vol = deflector.volume_mm3
        assert vol == 160.0 * 100.0 * 30.0

    def test_invalid_x_range(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="bad", obstacle_type=ObstacleType.CUSTOM,
                x_min_mm=100, x_max_mm=50,
                y_min_mm=0, y_max_mm=10,
                z_min_mm=0, z_max_mm=100,
            )

    def test_invalid_y_range(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="bad", obstacle_type=ObstacleType.CUSTOM,
                x_min_mm=0, x_max_mm=10,
                y_min_mm=100, y_max_mm=50,
                z_min_mm=0, z_max_mm=100,
            )

    def test_invalid_z_range(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="bad", obstacle_type=ObstacleType.CUSTOM,
                x_min_mm=0, x_max_mm=10,
                y_min_mm=0, y_max_mm=10,
                z_min_mm=100, z_max_mm=50,
            )


# ============================================================================
# Geometry Engine Tests (3D)
# ============================================================================

class TestPointInBox:
    def test_point_inside(self):
        box = (-10, 10, -10, 10, -10, 10)
        assert point_in_box(0, 0, 0, box) is True
        assert point_in_box(5, -5, 3, box) is True

    def test_point_outside(self):
        box = (-10, 10, -10, 10, -10, 10)
        assert point_in_box(20, 0, 0, box) is False
        assert point_in_box(0, 20, 0, box) is False
        assert point_in_box(0, 0, 20, box) is False

    def test_point_on_border(self):
        box = (-10, 10, -10, 10, -10, 10)
        assert point_in_box(10, 0, 0, box) is False


class TestPointInObstacle:
    def test_inside_expanded(self, deflector):
        assert point_in_obstacle(-82, 0, 220, deflector, use_expanded=True) is True
        assert point_in_obstacle(0, -52, 220, deflector, use_expanded=True) is True

    def test_outside_expanded(self, deflector):
        assert point_in_obstacle(0, 0, 200, deflector, use_expanded=True) is False
        assert point_in_obstacle(100, 100, 100, deflector, use_expanded=True) is False

    def test_inside_original(self, deflector):
        assert point_in_obstacle(0, 0, 220, deflector, use_expanded=False) is True


class TestDistanceToBoxBorder:
    def test_outside_distance(self):
        box = (-10, 10, -10, 10, -10, 10)
        dist = distance_to_box_border(15, 0, 0, box)
        assert abs(dist - 5.0) < 0.01

    def test_inside_depth(self):
        box = (-10, 10, -10, 10, -10, 10)
        dist = distance_to_box_border(5, 0, 0, box)
        assert abs(dist - (-5.0)) < 0.01

    def test_corner_distance(self):
        box = (-10, 10, -10, 10, -10, 10)
        dist = distance_to_box_border(15, 15, 0, box)
        expected = (5**2 + 5**2) ** 0.5
        assert abs(dist - expected) < 0.01


class TestMinClearance:
    def test_no_obstacles(self):
        assert min_clearance_to_obstacles(0, 0, 0, []) == float("inf")

    def test_clear_point(self, deflector):
        margin = min_clearance_to_obstacles(0, 0, 100, [deflector])
        assert margin > 0

    def test_inside_obstacle(self, deflector):
        margin = min_clearance_to_obstacles(0, 0, 220, [deflector])
        assert margin < 0


class TestSegmentCollision:
    def test_clear_segment(self):
        box = (-10, 10, -10, 10, -10, 10)
        assert segment_collides_with_box(-50, 0, 0, 50, 0, 0, box) is True

    def test_segment_above(self):
        box = (-10, 10, -10, 10, -10, 10)
        assert segment_collides_with_box(-50, 0, 50, 50, 0, 50, box) is False

    def test_segment_misses_in_y(self):
        box = (-10, 10, -10, 10, -10, 10)
        assert segment_collides_with_box(-50, 50, 0, 50, 50, 0, box) is False


class TestExpandWithGlobalClearance:
    def test_global_expansion(self, deflector):
        expanded = expand_obstacles_with_global_clearance([deflector], 10.0)
        assert len(expanded) == 1
        x_min, x_max, y_min, y_max, z_min, z_max = expanded[0]
        assert x_min == pytest.approx(-95.0)
        assert x_max == pytest.approx(95.0)
        assert y_min == pytest.approx(-65.0)
        assert y_max == pytest.approx(65.0)
        assert z_min == pytest.approx(195.0)
        assert z_max == pytest.approx(255.0)


class TestHighestObstacleZ:
    def test_no_obstacles(self):
        assert find_highest_obstacle_z([]) == 0.0

    def test_with_obstacles(self, deflector, baffle):
        z = find_highest_obstacle_z([deflector, baffle])
        # deflector is excluded by default, only baffle counts: 260 + 5 = 265
        assert z == 265.0

    def test_with_global_clearance(self, baffle):
        z = find_highest_obstacle_z([baffle], global_clearance_mm=10.0)
        # baffle: 260 + 5 + 10 = 275
        assert z == 275.0

    def test_deflector_excluded_by_default(self, deflector):
        # Deflector should be excluded by default
        z = find_highest_obstacle_z([deflector])
        assert z == 0.0

    def test_deflector_included_when_not_excluded(self, deflector):
        # But can be included if explicitly requested
        z = find_highest_obstacle_z([deflector], exclude_types=[])
        assert z == 245.0  # 240 + 5


class TestSafeCorridor3D:
    def test_empty_obstacles(self, mould):
        corridor = estimate_safe_corridor_3d(mould, [], 10.0)
        assert corridor is not None

    def test_with_obstacles(self, mould_3d, baffle):
        funnel = ObstacleEnvelope(
            name="Funnel", obstacle_type=ObstacleType.FUNNEL_MECHANISM,
            x_min_mm=40.0, x_max_mm=120.0,
            y_min_mm=0.0, y_max_mm=60.0,
            z_min_mm=160.0, z_max_mm=260.0,
            clearance_mm=5.0,
        )
        corridor = estimate_safe_corridor_3d(
            mould_3d, [baffle, funnel], 10.0,
            x_search_range_mm=200.0, y_search_range_mm=200.0,
        )
        if corridor is not None:
            (c_x_min, c_x_max), (c_y_min, c_y_max) = corridor
            assert c_x_min < c_x_max
            assert c_y_min < c_y_max


class TestObstacleBoundsInXY:
    def test_no_intersection(self, mould):
        obs = ObstacleEnvelope(
            name="High", obstacle_type=ObstacleType.CUSTOM,
            x_min_mm=-10, x_max_mm=10,
            y_min_mm=-10, y_max_mm=10,
            z_min_mm=500, z_max_mm=600,
            clearance_mm=0,
        )
        x_ranges, y_ranges = find_obstacle_bounds_in_xy([obs], 0.0, mould.mould_top_z_mm)
        assert len(x_ranges) == 0
        assert len(y_ranges) == 0

    def test_with_intersection(self, deflector):
        x_ranges, y_ranges = find_obstacle_bounds_in_xy([deflector], 0.0, 220.0)
        assert len(x_ranges) > 0
        assert len(y_ranges) > 0