# RobotSwabbing Engineering Report

**Project:** IS_Machine_BlankSide_Example
**Date:** 2026-06-26 11:02:58
**Feasible:** YES


## SAFETY WARNINGS

**This software is an engineering support tool, NOT a certified safety system.**

- Final trajectory MUST be validated by robot simulation or real dry-run at low speed.
- Final robot path MUST be validated against the real FANUC robot reachability and axis limits.
- The system does NOT replace machine risk assessment.
- Collision checks are valid ONLY for the geometry entered by the user.
- Safety clearances MUST be reviewed by a qualified mechanical/automation engineer.
- Any real implementation on an IS machine MUST be validated with lockout/tagout,
  dry-run, reduced speed and customer safety procedure.


## Mould Geometry

| Parameter | Value |
|-----------|-------|
| Mould Diameter | 150.0 mm |
| Mould Height | 120.0 mm |
| Neck Height | 20.0 mm |
| Mould Top Z | 200.0 mm |
| Mould Center X | 0.0 mm |
| Mould Bottom Z | 80.0 mm |

## Obstacles

| Name | Type | X min | X max | Z min | Z max | Clearance |
|------|------|-------|-------|-------|-------|-----------|
| Upper Wire / Mould Edge | mould_upper_edge | -75.0 | 75.0 | 195.0 | 205.0 | 5.0 mm |
| Deflector Left Side | deflector | -200.0 | -85.0 | 210.0 | 240.0 | 8.0 mm |
| Deflector Right Side | deflector | 85.0 | 200.0 | 210.0 | 240.0 | 8.0 mm |
| Baffle Mechanism | baffle_mechanism | -200.0 | -90.0 | 150.0 | 270.0 | 5.0 mm |
| Funnel Mechanism | funnel_mechanism | 90.0 | 200.0 | 150.0 | 270.0 | 5.0 mm |
| Machine Frame Left | machine_frame | -300.0 | -250.0 | 0.0 | 400.0 | 10.0 mm |
| Machine Frame Right | machine_frame | 250.0 | 300.0 | 0.0 | 400.0 | 10.0 mm |

## Robot / Swabbing Parameters

| Parameter | Value |
|-----------|-------|
| Lance Length | 250 mm |
| Nozzle Offset | 0.0 mm |
| Spray Cone Angle | 30.0 deg |
| Target Spray Distance | 50.0 mm |
| Minimum Clearance | 10.0 mm |
| Nominal Speed | 200.0 mm/s |
| Min Speed | 50.0 mm/s |
| Max Speed | 500.0 mm/s |
| Valve Delay | 50.0 ms |
| Coating Target | 1.00 |

## Calculated Trajectory

Total points: 22
Min clearance margin: 6.00

| ID | X [mm] | Z [mm] | Speed [mm/s] | Valve | Segment | Collision | Margin [mm] | Note |
|----|--------|--------|-------------|-------|---------|----------|-------------|------|
| 0 | 224.0 | 470.0 | 200.0 | OFF | wait | clear | 50.36 | Wait position — safe height above obstacles |
| 1 | 224.0 | 420.0 | 200.0 | OFF | approach | warning | 6.00 | Approach step 1/5 |
| 2 | 224.0 | 370.0 | 200.0 | OFF | approach | warning | 6.00 | Approach step 2/5 |
| 3 | 224.0 | 320.0 | 200.0 | OFF | approach | warning | 6.00 | Approach step 3/5 |
| 4 | 224.0 | 270.0 | 200.0 | OFF | approach | warning | 6.00 | Approach step 4/5 |
| 5 | 224.0 | 220.0 | 200.0 | OFF | approach | warning | 6.00 | Approach step 5/5 |
| 6 | 224.0 | 200.0 | 200.0 | OFF | enter | warning | 6.00 | Entry — top of mould cavity |
| 7 | 224.0 | 200.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=200.0 | Advance: 10.0mm |
| 8 | 224.0 | 190.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=190.0 |
| 9 | 224.0 | 180.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=180.0 |
| 10 | 224.0 | 170.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=170.0 |
| 11 | 224.0 | 160.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=160.0 |
| 12 | 224.0 | 150.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=150.0 |
| 13 | 224.0 | 140.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=140.0 |
| 14 | 224.0 | 130.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=130.0 |
| 15 | 224.0 | 120.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=120.0 |
| 16 | 224.0 | 110.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=110.0 |
| 17 | 224.0 | 100.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=100.0 |
| 18 | 224.0 | 90.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down Z=90.0 |
| 19 | 224.0 | 80.0 | 200.0 | ON | swab_down | warning | 6.00 | Swab down — bottom Z=80.0 |
| 20 | 224.0 | 215.0 | 200.0 | OFF | exit | warning | 6.00 | Exit — above mould top with clearance |
| 21 | 224.0 | 470.0 | 200.0 | OFF | exit | clear | 50.36 | Return to wait position |

## Collision Warnings

- Point 1 (224.0, 420.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 2 (224.0, 370.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 3 (224.0, 320.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 4 (224.0, 270.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 5 (224.0, 220.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 6 (224.0, 200.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 7 (224.0, 200.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 8 (224.0, 190.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 9 (224.0, 180.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 10 (224.0, 170.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 11 (224.0, 160.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 12 (224.0, 150.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 13 (224.0, 140.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 14 (224.0, 130.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 15 (224.0, 120.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 16 (224.0, 110.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 17 (224.0, 100.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 18 (224.0, 90.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 19 (224.0, 80.0) WARNING — close to obstacle (margin: 6.0 mm)
- Point 20 (224.0, 215.0) WARNING — close to obstacle (margin: 6.0 mm)

## Validation Checklist

- [ ] Trajectory reviewed by automation engineer
- [ ] Obstacle geometry verified against machine drawings
- [ ] Safety clearances confirmed by mechanical engineer
- [ ] Robot reachability verified (FANUC Robot Simulation / ROBOGUIDE)
- [ ] Dry-run executed at reduced speed
- [ ] Lockout/Tagout procedure followed
- [ ] Customer safety procedure applied
- [ ] Coating thickness measured and verified
- [ ] Valve timing verified on machine
- [ ] Final sign-off by responsible engineer
