# RobotSimulator — System Architecture

## 1. Overview

RobotSimulator is a Python engineering application for calculating safe X-Z swabbing
trajectories for a FANUC robot on the blank side of an IS hollow glass forming machine.

## 2. Architecture Layers

```
+--------------------------------------------------------------+
|                    Streamlit UI (app.py)                      |
+------------------+-------------------+-----------------------+
                   |                   |
          +--------v--------+  +-------v-------+
          | Trajectory      |  | Valve Timing  |
          | (trajectory.py) |  | (valve_timing)|
          +--------+--------+  +-------+-------+
                   |                   |
          +--------v------------------v-------+
          |       Velocity Modulation         |
          +----------------+-----------------+
                           |
          +----------------v-----------------+
          |       Collision Detection        |
          +----------------+-----------------+
                           |
          +----------------v-----------------+
          |       Geometry Engine            |
          +----------------+-----------------+
                           |
          +----------------v-----------------+
          |       Data Models                |
          +----------------------------------+
```

## 3. File Structure

```
RobotSimulator/
    README.md
    requirements.txt
    app.py
    memory.md
    data/
    robotsimulator/
        __init__.py
        models.py        # Dataclasses with validation
        geometry.py      # 2D geometry operations
        collision.py     # Collision detection
        trajectory.py    # Trajectory generator
        velocity.py      # Velocity modulation
        valve_timing.py  # Valve ON/OFF timing
        export.py        # CSV / JSON / Report MD export
        plotting.py      # Matplotlib X-Z plot
    tests/
        test_geometry.py
        test_collision.py
        test_trajectory.py
    docs/
    outputs/
```

## 4. Coordinate System

- X axis: horizontal, 0 at mould centerline, positive toward robot (blank side)
- Z axis: vertical, 0 at machine datum, positive upward
- Y axis (future): not modeled in v1

## 5. Data Model

- MouldGeometry: mould dimensions and position
- ObstacleEnvelope: rectangular forbidden zones
- RobotParameters: lance, speed, valve settings
- SwabbingParameters: process-specific settings
- TrajectoryPoint: single X-Z point with state
- TrajectoryResult: complete trajectory output

## 6. Calculation Flow

1. Geometry validation
2. Obstacle expansion (clearance applied)
3. Highest obstacle Z detected
4. Wait position computed
5. Approach positions computed
6. Entry position computed (avoiding deflector/baffle/funnel)
7. Swab down points generated along mould centerline
8. Exit position computed
9. Velocity modulation applied per point
10. Valve ON/OFF timing applied
11. Collision check on all points and segments
12. Optional offset retry if collision found
13. Final result returned with warnings
