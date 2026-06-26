# RobotSimulator — Development Memory

## Project
FANUC robot swabbing trajectory calculator for IS hollow glass machine blank side.

## Coordinate System
- X: horizontal, 0 at mould centerline, positive toward robot
- Z: vertical, 0 at machine datum, positive upward
- All dimensions in mm

## Key Decisions
- Lance orientation: vertical (first model)
- Mould diameter: constant (cylindrical mould V1)
- Swabbing: swab_down as default, swab_up optional
- Entry: from above
- Single section for V1
- FANUC TP/KAREL export: placeholder only
- DXF/DWG import: placeholder only
- Obstacles: rectangular V1, polygon future
