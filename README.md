# RobotSimulator

[![Version](https://img.shields.io/badge/version-0.2.0-blue)](https://github.com/BotteroGroup/RobotSimulator/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-59%20passed-green)](https://github.com/BotteroGroup/RobotSimulator/actions)
[![License](https://img.shields.io/badge/license-Proprietary-red)](LICENSE)

## FANUC Robot Swabbing Trajectory Calculator for IS Hollow Glass Forming Machine — Blank Side

**Version:** v0.2.0 (build 2026-06-26)  
**Status:** Engineering Tool — Not for Production Use  
**License:** Proprietary — Bottero Group S.p.A.

Engineering application for configuring and calculating ideal X-Z swabbing trajectories
for a FANUC robot used to swab the blank side of an IS (Individual Section) hollow glass
forming machine.

### WARNING — SAFETY NOTICE

- **This software is an engineering support tool, NOT a certified safety system.**
- Final trajectory MUST be validated by robot simulation or real dry-run at low speed.
- Final robot path MUST be validated against the real FANUC robot reachability and axis limits.
- The system does NOT replace machine risk assessment.
- Collision checks are valid ONLY for the geometry entered by the user.
- Safety clearances MUST be reviewed by a qualified mechanical/automation engineer.
- Any real implementation on an IS machine MUST be validated with lockout/tagout,
  dry-run, reduced speed and customer safety procedure.

### Features

- Input form for machine and mould geometry
- Input form for obstacle/envelope definition
- Lance length selector (200 / 250 / 300 mm)
- Safety clearance parameter
- Spray/nozzle working distance parameter
- Robot trajectory calculation engine
- Collision check against obstacle envelopes
- X-Z trajectory output
- Velocity modulation calculation (uniform coating)
- Valve ON/OFF working area calculation
- Export of calculated points (CSV, JSON)
- Visualization of mould, obstacles and trajectory (matplotlib)
- Engineering report generation (Markdown)

### Project Structure

```
RobotSimulator/
    README.md
    requirements.txt
    app.py                         # Streamlit entry point
    memory.md                      # Development memory
    data/                          # Sample configurations
        sample_machine_config.json
        sample_obstacles.json
        sample_trajectory_output.csv
    robotsimulator/                # Core Python package
        __init__.py
        models.py                  # Data models (dataclasses + validation)
        geometry.py                # 2D X-Z geometry engine
        collision.py               # Collision detection
        trajectory.py              # Trajectory generation
        velocity.py                # Velocity modulation
        valve_timing.py            # Valve timing calculation
        export.py                  # CSV / JSON / Report export
        plotting.py                # Matplotlib X-Z visualization
    tests/                         # pytest unit tests
        test_geometry.py
        test_collision.py
        test_trajectory.py
    docs/                          # Technical documentation
        architecture.md
        user_guide.md
        engineering_notes.md
        validation_plan.md
    outputs/                       # Generated output files
```

### Installation

```bash
cd RobotSimulator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage — Streamlit (recommended)

```bash
cd RobotSimulator
source venv/bin/activate
streamlit run app.py
```

### Usage — Command Line (fallback)

```python
from robotsimulator.models import MouldGeometry, ObstacleEnvelope, RobotParameters
from robotsimulator.trajectory import generate_trajectory
from robotsimulator.export import export_csv, export_json, generate_report

# Define geometry, obstacles, parameters...
# result = generate_trajectory(mould, obstacles, robot_params)
# export_csv(result, "outputs/trajectory_export.csv")
```

### Coordinate System

- **X axis**: horizontal, 0 at mould centerline, positive toward robot side
- **Z axis**: vertical, 0 at machine datum, positive upward
- **All dimensions in millimeters**

### Development Status

- [x] Phase 1: Architecture & Design
- [ ] Phase 2: Project Scaffold
- [ ] Phase 3: Data Models
- [ ] Phase 4: Geometry Engine
- [ ] Phase 5: Collision Detection
- [ ] Phase 6: Trajectory Generation
- [ ] Phase 7: Velocity Modulation
- [ ] Phase 8: Valve Timing
- [ ] Phase 9: Export System
- [ ] Phase 10: Visualization
- [ ] Phase 11: Streamlit UI
- [ ] Phase 12: Unit Tests
- [ ] Phase 13: Documentation
- [ ] Phase 14: Sample Data & Integration

### License

Internal engineering tool — Bottero / Hollow Glass Division.
All rights reserved.
