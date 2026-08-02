import os
import pytest
import numpy as np
from robotsimulator.models import (
    MouldGeometry,
    ObstacleEnvelope,
    ObstacleType,
    TrajectoryResult,
    TrajectoryPoint,
    CollisionStatus,
    ValveState,
    SegmentType,
)
from robotsimulator.plotting import create_trajectory_plot_3d_interactive

# Path to the sample STL file
SAMPLE_STL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_cube.stl')

def test_plotting_with_stl_obstacle():
    """Test that the interactive 3D plot can be generated with an STL obstacle."""
    # Skip if plotly is not available (should be available in the environment)
    try:
        import plotly
    except ImportError:
        pytest.skip("Plotly not installed")

    # Create an obstacle from the STL file
    obstacle = ObstacleEnvelope.from_stl(
        filepath=SAMPLE_STL_PATH,
        name="Test STL Obstacle",
        obstacle_type=ObstacleType.CUSTOM,
        clearance_mm=2.0,
        reference_point=(0.0, 0.0, 0.0)
    )

    # Create a simple mould
    mould = MouldGeometry(
        mould_diameter_mm=100.0,
        mould_height_mm=50.0,
        neck_height_mm=5.0,
        mould_top_z_mm=0.0,
    )

    # Create a minimal trajectory result with a single clear point
    points = [
        TrajectoryPoint(
            point_id=0,
            x_mm=0.0,
            y_mm=0.0,
            z_mm=10.0,
            speed_mm_s=100.0,
            valve_state=ValveState.OFF,
            segment_type=SegmentType.WAIT,
            collision_status=CollisionStatus.CLEAR,
        )
    ]
    result = TrajectoryResult(points=points)

    # Generate the plot - this should not raise an exception
    fig = create_trajectory_plot_3d_interactive(
        mould=mould,
        obstacles=[obstacle],
        result=result,
        global_clearance_mm=0.0,
        title="Test Plot with STL Obstacle",
    )

    # Basic assertions: we got a plotly figure
    assert fig is not None
    # Check that the figure has at least one trace (the mesh should be added)
    assert len(fig.data) > 0

    # Optionally, we can check for the presence of a Mesh3d trace (our STL mesh)
    # Note: the order of traces is not guaranteed, so we look for any Mesh3d
    has_mesh = any(trace.type == 'mesh3d' for trace in fig.data)
    assert has_mesh, "Expected to find a Mesh3d trace for the STL obstacle"