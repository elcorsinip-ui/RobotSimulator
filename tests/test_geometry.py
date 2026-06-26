"""
RobotSimulator — Unit Tests for Geometry Engine
"""

import pytest
from robotsimulator.models import MouldGeometry, ObstacleEnvelope, ObstacleType
from robotsimulator.geometry import (
    expand_obstacle,
    expand_obstacles_with_global_clearance,
    point_in_rect,
    point_in_obstacle,
    point_in_any_obstacle,
    distance_to_rect_border,
    min_clearance_to_obstacles,
    segment_collides_with_rect,
    segment_clearance_check,
    estimate_safe_corridor,
    find_highest_obstacle_z,
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
    )


@pytest.fixture
def deflector():
    return ObstacleEnvelope(
        name="Test Deflector",
        obstacle_type=ObstacleType.DEFLECTOR,
        x_min_mm=-80.0,
        x_max_mm=80.0,
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
        z_min_mm=160.0,
        z_max_mm=260.0,
        clearance_mm=5.0,
    )


# ============================================================================
# Mould Geometry Tests
# ============================================================================

class TestMouldGeometry:
    def test_basic_creation(self, mould):
        assert mould.mould_diameter_mm == 150.0
        assert mould.mould_height_mm == 120.0
        assert mould.neck_height_mm == 20.0

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

    def test_negative_neck_height(self):
        with pytest.raises(ValueError):
            MouldGeometry(mould_diameter_mm=100, mould_height_mm=50, neck_height_mm=-5)


# ============================================================================
# Obstacle Envelope Tests
# ============================================================================

class TestObstacleEnvelope:
    def test_basic_creation(self, deflector):
        assert deflector.name == "Test Deflector"
        assert deflector.obstacle_type == ObstacleType.DEFLECTOR

    def test_expanded_envelope(self, deflector):
        assert deflector.expanded_x_min_mm == -85.0   # -80 - 5
        assert deflector.expanded_x_max_mm == 85.0    # 80 + 5
        assert deflector.expanded_z_min_mm == 205.0   # 210 - 5
        assert deflector.expanded_z_max_mm == 245.0   # 240 + 5

    def test_center_and_dimensions(self, deflector):
        assert deflector.center_x_mm == 0.0
        assert deflector.center_z_mm == 225.0
        assert deflector.width_mm == 160.0
        assert deflector.height_mm == 30.0

    def test_invalid_x_range(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="bad", obstacle_type=ObstacleType.CUSTOM,
                x_min_mm=100, x_max_mm=50, z_min_mm=0, z_max_mm=100,
            )

    def test_invalid_z_range(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="bad", obstacle_type=ObstacleType.CUSTOM,
                x_min_mm=0, x_max_mm=100, z_min_mm=100, z_max_mm=50,
            )

    def test_empty_name(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="", obstacle_type=ObstacleType.CUSTOM,
                x_min_mm=0, x_max_mm=10, z_min_mm=0, z_max_mm=10,
            )

    def test_string_obstacle_type_converted(self):
        # Pass string instead of enum — should be auto-converted
        obs = ObstacleEnvelope(
            name="test", obstacle_type="baffle_mechanism",
            x_min_mm=0, x_max_mm=10, z_min_mm=0, z_max_mm=10,
            clearance_mm=2,
        )
        assert obs.obstacle_type == ObstacleType.BAFFLE_MECHANISM

    def test_invalid_string_type_raises(self):
        with pytest.raises(ValueError):
            ObstacleEnvelope(
                name="test", obstacle_type="not_a_valid_type",
                x_min_mm=0, x_max_mm=10, z_min_mm=0, z_max_mm=10,
            )


# ============================================================================
# Geometry Engine Tests
# ============================================================================

class TestPointInRect:
    def test_point_inside(self):
        assert point_in_rect(0, 0, (-10, 10, -10, 10)) is True

    def test_point_outside(self):
        assert point_in_rect(20, 0, (-10, 10, -10, 10)) is False

    def test_point_on_border(self):
        # Strictly inside: border points return False
        assert point_in_rect(10, 0, (-10, 10, -10, 10)) is False


class TestPointInObstacle:
    def test_inside_expanded(self, deflector):
        # Point inside expanded zone
        assert point_in_obstacle(-82, 220, deflector, use_expanded=True) is True

    def test_outside_expanded(self, deflector):
        # Point outside expanded zone
        assert point_in_obstacle(0, 200, deflector, use_expanded=True) is False

    def test_inside_original(self, deflector):
        # Point inside original (not expanded)
        assert point_in_obstacle(0, 220, deflector, use_expanded=False) is True


class TestDistanceToRectBorder:
    def test_outside_distance(self):
        # Point at (15, 0), rect from -10 to 10
        dist = distance_to_rect_border(15, 0, (-10, 10, -10, 10))
        assert abs(dist - 5.0) < 0.01

    def test_inside_depth(self):
        # Point at (5, 0), rect from -10 to 10
        dist = distance_to_rect_border(5, 0, (-10, 10, -10, 10))
        assert abs(dist - (-5.0)) < 0.01  # 5mm deep inside


class TestMinClearance:
    def test_no_obstacles(self):
        assert min_clearance_to_obstacles(0, 0, []) == float("inf")

    def test_clear_point(self, deflector):
        # Point far below deflector
        margin = min_clearance_to_obstacles(0, 100, [deflector])
        assert margin > 0

    def test_inside_obstacle(self, deflector):
        margin = min_clearance_to_obstacles(0, 220, [deflector])
        assert margin < 0


class TestSegmentCollision:
    def test_clear_segment(self):
        rect = (-10, 10, -10, 10)
        assert segment_collides_with_rect(-50, 0, 50, 0, rect) is True

    def test_segment_above(self):
        rect = (-10, 10, -10, 10)
        assert segment_collides_with_rect(-50, 50, 50, 50, rect) is False


class TestExpandWithGlobalClearance:
    def test_global_expansion(self, deflector):
        expanded = expand_obstacles_with_global_clearance([deflector], 10.0)
        assert len(expanded) == 1
        x_min, x_max, z_min, z_max = expanded[0]
        # Original x_min=-80, clearance 5 + global 10 = 15
        assert x_min == pytest.approx(-95.0)
        assert x_max == pytest.approx(95.0)


class TestHighestObstacleZ:
    def test_no_obstacles(self):
        assert find_highest_obstacle_z([]) == 0.0

    def test_with_obstacles(self, deflector, baffle):
        # Baffle goes up to Z=260 + clearance 5 = 265
        z = find_highest_obstacle_z([deflector, baffle])
        assert z == 265.0

    def test_with_global_clearance(self, deflector):
        # Deflector z_max=240, clearance=5, global=10 -> 255
        z = find_highest_obstacle_z([deflector], global_clearance_mm=10.0)
        assert z == 255.0


class TestSafeCorridor:
    def test_empty_obstacles(self, mould):
        corridor = estimate_safe_corridor(mould, [], 10.0)
        assert corridor is not None

    def test_with_blocking_obstacles(self, mould, baffle):
        funnel = ObstacleEnvelope(
            name="Funnel",
            obstacle_type=ObstacleType.FUNNEL_MECHANISM,
            x_min_mm=40.0,
            x_max_mm=120.0,
            z_min_mm=160.0,
            z_max_mm=260.0,
            clearance_mm=5.0,
        )
        corridor = estimate_safe_corridor(
            mould, [baffle, funnel], 10.0,
            x_search_range_mm=200.0,
        )
        if corridor is not None:
            c_x_min, c_x_max = corridor
            assert c_x_min < c_x_max
