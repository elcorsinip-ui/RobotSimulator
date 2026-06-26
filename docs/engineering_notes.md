# RobotSimulator — Engineering Notes

## First-Order Velocity Model

```
relative_surface_factor = local_diameter_mm / reference_diameter_mm
raw_speed = nominal_speed_mm_s / relative_surface_factor
speed = clamp(raw_speed, min_speed, max_speed)
```

This achieves approximately uniform coating thickness assuming
flow rate is constant.

## First-Order Valve Timing

```
valve_advance_distance_mm = speed_mm_s * valve_delay_ms / 1000
valve_on_z = coating_start_z + advance_distance  (when coming from above)
valve_off_z = coating_end_z - advance_distance   (conservative)
```

## Collision Detection

- All obstacles expanded by their clearance + global clearance
- Each trajectory point checked against all expanded rectangles
- Each segment between points sampled (20 samples default)
- Warnings issued if margin < 1.5x clearance

## Limitations (v1)

- Only rectangular obstacles (polygons planned for v2)
- Constant mould diameter (variable profile planned)
- Vertical lance orientation only (tilt planned)
- Approximate coating model — needs real calibration
