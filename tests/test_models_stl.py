import os
import pytest
from robotsimulator.models import ObstacleEnvelope, ObstacleType

# Path to the sample STL file we created
SAMPLE_STL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_cube.stl')

def test_obstacle_envelope_from_stl_success():
    """Test creating an ObstacleEnvelope from a valid STL file."""
    # We'll use a known point as reference
    reference_point = (10.0, 20.0, 30.0)
    obstacle = ObstacleEnvelope.from_stl(
        filepath=SAMPLE_STL_PATH,
        name="Test STL Obstacle",
        obstacle_type=ObstacleType.CUSTOM,
        clearance_mm=5.0,
        reference_point=reference_point
    )
    
    # The sample cube is 10x10x10 with min corner at (0,0,0) and max at (10,10,10)
    # After applying the reference point, the bounding box should be:
    # x: [10+0, 10+10] = [10, 20]
    # y: [20+0, 20+10] = [20, 30]
    # z: [30+0, 30+10] = [30, 40]
    assert obstacle.name == "Test STL Obstacle"
    assert obstacle.obstacle_type == ObstacleType.CUSTOM
    assert obstacle.clearance_mm == 5.0
    assert obstacle.stl_path == SAMPLE_STL_PATH
    
    # Check the bounding box (without clearance)
    assert obstacle.x_min_mm == 10.0
    assert obstacle.x_max_mm == 20.0
    assert obstacle.y_min_mm == 20.0
    assert obstacle.y_max_mm == 30.0
    assert obstacle.z_min_mm == 30.0
    assert obstacle.z_max_mm == 40.0
    
    # Check the expanded bounding box (with clearance)
    assert obstacle.expanded_x_min_mm == 5.0   # 10 - 5
    assert obstacle.expanded_x_max_mm == 25.0  # 20 + 5
    assert obstacle.expanded_y_min_mm == 15.0  # 20 - 5
    assert obstacle.expanded_y_max_mm == 35.0  # 30 + 5
    assert obstacle.expanded_z_min_mm == 25.0  # 30 - 5
    assert obstacle.expanded_z_max_mm == 45.0  # 40 + 5

def test_obstacle_envelope_from_stl_file_not_found():
    """Test that a non-existent STL file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        ObstacleEnvelope.from_stl(
            filepath="non_existent_file.stl",
            name="Test",
            obstacle_type=ObstacleType.CUSTOM,
            clearance_mm=0.0
        )

def test_obstacle_envelope_from_stl_import_error(monkeypatch):
    """Test that if the stl module is not available, an ImportError is raised."""
    # We'll mock the import of 'stl' in the robotsimulator.models module to raise ImportError
    import robotsimulator.models as models
    original_import = __import__

    def mock_import(name, *args, **kwargs):
        if name == 'stl':
            raise ImportError("No module named 'stl'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr('builtins.__import__', mock_import)

    with pytest.raises(ImportError, match="numpy-stl package is required"):
        ObstacleEnvelope.from_stl(
            filepath=SAMPLE_STL_PATH,
            name="Test",
            obstacle_type=ObstacleType.CUSTOM,
            clearance_mm=0.0
        )

def test_obstacle_envelope_post_init_with_stl_path():
    """Test that the __post_init__ method validates the stl_path if provided."""
    # Valid case: file exists
    obstacle = ObstacleEnvelope(
        name="Test",
        obstacle_type=ObstacleType.CUSTOM,
        x_min_mm=0, x_max_mm=10,
        y_min_mm=0, y_max_mm=10,
        z_min_mm=0, z_max_mm=10,
        clearance_mm=0.0,
        stl_path=SAMPLE_STL_PATH
    )
    # Should not raise
    assert obstacle.stl_path == SAMPLE_STL_PATH
    
    # Invalid case: file does not exist
    with pytest.raises(FileNotFoundError):
        ObstacleEnvelope(
            name="Test",
            obstacle_type=ObstacleType.CUSTOM,
            x_min_mm=0, x_max_mm=10,
            y_min_mm=0, y_max_mm=10,
            z_min_mm=0, z_max_mm=10,
            clearance_mm=0.0,
            stl_path="non_existent.stl"
        )
    
    # Invalid case: stl_path is not a string
    with pytest.raises(ValueError, match="stl_path must be a string"):
        ObstacleEnvelope(
            name="Test",
            obstacle_type=ObstacleType.CUSTOM,
            x_min_mm=0, x_max_mm=10,
            y_min_mm=0, y_max_mm=10,
            z_min_mm=0, z_max_mm=10,
            clearance_mm=0.0,
            stl_path=123
        )

if __name__ == "__main__":
    pytest.main([__file__, "-v"])