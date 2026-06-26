# RobotSimulator — Validation Plan

## Unit Testing
59 unit tests covering:
- Mould geometry validation
- Obstacle validation and string-to-enum conversion
- Point-in-rectangle and segment-rectangle collisions
- Safe corridor estimation
- Trajectory generation and segment ordering
- Velocity calculation (clamping, factor)
- Valve timing calculations

Run: `cd /root/RobotSimulator && pytest tests/ -v`

## Integration Testing
End-to-end test with sample machine config and obstacles:
1. Load JSON config and obstacles
2. Generate trajectory
3. Verify feasibility
4. Export CSV, JSON, MD report

## Pre-Production Validation Checklist

- [ ] Trajectory validated by robot offline simulation (e.g., FANUC ROBOGUIDE)
- [ ] Reachability verified against real robot workspace
- [ ] Joint limits checked
- [ ] Cycle time calculated
- [ ] Dry-run at 10% speed on real machine with safe test setup
- [ ] All obstacles verified against actual machine geometry
- [ ] Safety clearances reviewed by mechanical engineer
- [ ] Risk assessment updated
- [ ] Customer safety procedure followed

## Safety

This tool is NOT a certified safety system.
Always follow lockout/tagout and customer safety procedures.
