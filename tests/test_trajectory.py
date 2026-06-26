"""
RobotSimulator — Unit Tests for Trajectory Generation
"""

import pytest
from robotsimulator.models import (
    MouldGeometry,
    ObstacleEnvelope,
    ObstacleType,
    RobotParameters,
    SwabbingParameters,
    TrajectoryResult,
    CollisionStatus,
    SegmentType,
    ValveState,
)
from robotsimulator.trajectory import generate_trajectory
from robotsimulator.velocity import calculate_velocity, apply_velocity_profile
from robotsimulator.valve_timing import (
    calculate_valve_advance_distance,
    calculate_valve_on_position,
    calculate_valve_off_position,
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
def robot_params():
    return RobotParameters(
        lance_length_mm=250,
        nozzle_offset_mm=0.0,
        spray_cone_angle_deg=30.0,
        target_spray_distance_mm=50.0,
        minimum_clearance_mm=10.0,
        max_robot_speed_mm_s=500.0,
        min_robot_speed_mm_s=50.0,
        nominal_speed_mm_s=200.0,
        valve_delay_ms=50.0,
        coating_target_relative=1.0,
    )


@pytest.fixture
def swabbing_params():
    return SwabbingParameters(
        reference_diameter_mm=150.0,
        coating_start_z_mm=200.0,
        coating_end_z_mm=80.0,
        swab_step_mm=10.0,
        include_swab_up=False,
        approach_height_mm=50.0,
    )


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


# ============================================================================
# Trajectory Generation Tests
# ============================================================================

class TestGenerateTrajectory:
    def test_basic_trajectory(self, mould, robot_params, swabbing_params):
        result = generate_trajectory(
            mould, [], robot_params, swabbing_params,
        )
        assert result is not None
        assert result.total_points > 0
        assert result.feasible is True

    def test_trajectory_has_all_segment_types(self, mould, robot_params, swabbing_params):
        result = generate_trajectory(
            mould, [], robot_params, swabbing_params,
        )
        segment_types = {p.segment_type for p in result.points}
        assert SegmentType.WAIT in segment_types
        assert SegmentType.APPROACH in segment_types
        assert SegmentType.ENTER in segment_types
        assert SegmentType.SWAB_DOWN in segment_types
        assert SegmentType.EXIT in segment_types

    def test_trajectory_order(self, mould, robot_params, swabbing_params):
        result = generate_trajectory(
            mould, [], robot_params, swabbing_params,
        )
        # First point should be WAIT
        assert result.points[0].segment_type == SegmentType.WAIT
        # Last point should be EXIT
        assert result.points[-1].segment_type == SegmentType.EXIT

    def test_trajectory_with_obstacles(self, mould, obstacles, robot_params, swabbing_params):
        result = generate_trajectory(
            mould, obstacles, robot_params, swabbing_params,
        )
        assert result is not None
        assert result.total_points > 0

    def test_swab_points_inside_mould(self, mould, robot_params, swabbing_params):
        result = generate_trajectory(
            mould, [], robot_params, swabbing_params,
        )
        swab_pts = [p for p in result.points
                    if p.segment_type == SegmentType.SWAB_DOWN]
        for p in swab_pts:
            assert p.z_mm <= mould.mould_top_z_mm
            assert p.z_mm >= mould.mould_bottom_z_mm

    def test_trajectory_with_swab_up(self, mould, robot_params):
        params = SwabbingParameters(
            reference_diameter_mm=150.0,
            coating_start_z_mm=200.0,
            coating_end_z_mm=80.0,
            swab_step_mm=20.0,
            include_swab_up=True,
            approach_height_mm=50.0,
        )
        result = generate_trajectory(mould, [], robot_params, params)
        segment_types = {p.segment_type for p in result.points}
        assert SegmentType.SWAB_UP in segment_types


# ============================================================================
# Velocity Tests
# ============================================================================

class TestVelocity:
    def test_nominal_speed(self):
        speed = calculate_velocity(150.0, 150.0, 200.0, 50.0, 500.0)
        assert speed == 200.0  # Same diameter = nominal speed

    def test_larger_diameter_slower(self):
        speed = calculate_velocity(300.0, 150.0, 200.0, 50.0, 500.0)
        assert speed < 200.0  # Larger diameter = slower

    def test_smaller_diameter_faster(self):
        speed = calculate_velocity(75.0, 150.0, 200.0, 50.0, 500.0)
        assert speed > 200.0  # Smaller diameter = faster

    def test_speed_clamped_min(self):
        speed = calculate_velocity(10000.0, 150.0, 200.0, 50.0, 500.0)
        assert speed == 50.0  # Clamped to minimum

    def test_speed_clamped_max(self):
        speed = calculate_velocity(1.0, 150.0, 200.0, 50.0, 500.0)
        assert speed == 500.0  # Clamped to maximum

    def test_zero_reference_raises(self):
        with pytest.raises(ValueError):
            calculate_velocity(150.0, 0.0, 200.0, 50.0, 500.0)

    def test_zero_local_diameter(self):
        speed = calculate_velocity(0.0, 150.0, 200.0, 50.0, 500.0)
        assert speed == 500.0  # Returns max speed


# ============================================================================
# Valve Timing Tests
# ============================================================================

class TestValveTiming:
    def test_advance_distance(self):
        dist = calculate_valve_advance_distance(200.0, 50.0)
        assert abs(dist - 10.0) < 0.01  # 200 * 0.05 = 10

    def test_valve_on_from_above(self):
        # Robot comes from above, coating starts at Z=200
        z_on = calculate_valve_on_position(200.0, 200.0, 50.0, "from_above")
        assert z_on > 200.0  # Turn on above the start

    def test_valve_on_from_below(self):
        z_on = calculate_valve_on_position(200.0, 200.0, 50.0, "from_below")
        assert z_on < 200.0  # Turn on below the start

    def test_valve_off_conservative(self):
        z_off = calculate_valve_off_position(80.0, 200.0, 50.0,
                                               "from_above", False)
        assert z_off == 80.0  # Exact end position

    def test_valve_off_compensated(self):
        z_off = calculate_valve_off_position(80.0, 200.0, 50.0,
                                               "from_above", True)
        assert z_off > 80.0  # Close earlier

    def test_zero_delay(self):
        dist = calculate_valve_advance_distance(200.0, 0.0)
        assert dist == 0.0
