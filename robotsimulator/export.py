"""
RobotSimulator — Export System

Exports trajectory results to CSV, JSON, and Markdown engineering report.
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from typing import List, Optional

from .models import (
    MouldGeometry,
    ObstacleEnvelope,
    RobotParameters,
    SwabbingParameters,
    TrajectoryPoint,
    TrajectoryResult,
    ProjectConfiguration,
)


# ============================================================================
# CSV Export
# ============================================================================

def export_csv(
    result: TrajectoryResult,
    filepath: str,
) -> str:
    """
    Export trajectory points to a CSV file.

    Args:
        result: TrajectoryResult with points to export
        filepath: Output file path

    Returns:
        Absolute path to the created file.
    """
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "point_id",
            "x_mm",
            "z_mm",
            "speed_mm_s",
            "valve_state",
            "segment_type",
            "collision_status",
            "clearance_margin_mm",
            "note",
        ])

        for p in result.points:
            writer.writerow([
                p.point_id,
                f"{p.x_mm:.2f}",
                f"{p.z_mm:.2f}",
                f"{p.speed_mm_s:.2f}",
                p.valve_state.value,
                p.segment_type.value,
                p.collision_status.value,
                f"{p.clearance_margin_mm:.2f}" if p.clearance_margin_mm != float("inf") else "inf",
                p.note,
            ])

    return filepath


# ============================================================================
# JSON Export
# ============================================================================

def export_json(
    config: ProjectConfiguration,
    result: TrajectoryResult,
    filepath: str,
) -> str:
    """
    Export complete project configuration and trajectory to a JSON file.

    Args:
        config: Project configuration
        result: Trajectory result
        filepath: Output file path

    Returns:
        Absolute path to the created file.
    """
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    data = {
        "project_name": config.project_name,
        "export_timestamp": datetime.now().isoformat(),
        "mould_geometry": {
            "mould_diameter_mm": config.mould.mould_diameter_mm,
            "mould_height_mm": config.mould.mould_height_mm,
            "neck_height_mm": config.mould.neck_height_mm,
            "mould_top_z_mm": config.mould.mould_top_z_mm,
            "mould_center_x_mm": config.mould.mould_center_x_mm,
        },
        "obstacles": [
            {
                "name": obs.name,
                "type": obs.obstacle_type.value,
                "x_min_mm": obs.x_min_mm,
                "x_max_mm": obs.x_max_mm,
                "z_min_mm": obs.z_min_mm,
                "z_max_mm": obs.z_max_mm,
                "clearance_mm": obs.clearance_mm,
            }
            for obs in config.obstacles
        ],
        "robot_parameters": {
            "lance_length_mm": config.robot_params.lance_length_mm,
            "nozzle_offset_mm": config.robot_params.nozzle_offset_mm,
            "spray_cone_angle_deg": config.robot_params.spray_cone_angle_deg,
            "target_spray_distance_mm": config.robot_params.target_spray_distance_mm,
            "minimum_clearance_mm": config.robot_params.minimum_clearance_mm,
            "nominal_speed_mm_s": config.robot_params.nominal_speed_mm_s,
            "min_robot_speed_mm_s": config.robot_params.min_robot_speed_mm_s,
            "max_robot_speed_mm_s": config.robot_params.max_robot_speed_mm_s,
            "valve_delay_ms": config.robot_params.valve_delay_ms,
            "coating_target_relative": config.robot_params.coating_target_relative,
        },
        "trajectory": {
            "feasible": result.feasible,
            "total_points": result.total_points,
            "min_clearance_margin_mm": (
                f"{result.min_clearance_margin_mm:.2f}"
                if result.min_clearance_margin_mm != float("inf") else "inf"
            ),
            "collision_warnings": result.collision_warnings,
            "points": [
                {
                    "point_id": p.point_id,
                    "x_mm": round(p.x_mm, 2),
                    "z_mm": round(p.z_mm, 2),
                    "speed_mm_s": round(p.speed_mm_s, 2),
                    "valve_state": p.valve_state.value,
                    "segment_type": p.segment_type.value,
                    "collision_status": p.collision_status.value,
                    "clearance_margin_mm": (
                        round(p.clearance_margin_mm, 2)
                        if p.clearance_margin_mm != float("inf") else "inf"
                    ),
                    "note": p.note,
                }
                for p in result.points
            ],
        },
    }

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return filepath


# ============================================================================
# Markdown Engineering Report
# ============================================================================

_SAFETY_WARNINGS = """
## SAFETY WARNINGS

**This software is an engineering support tool, NOT a certified safety system.**

- Final trajectory MUST be validated by robot simulation or real dry-run at low speed.
- Final robot path MUST be validated against the real FANUC robot reachability and axis limits.
- The system does NOT replace machine risk assessment.
- Collision checks are valid ONLY for the geometry entered by the user.
- Safety clearances MUST be reviewed by a qualified mechanical/automation engineer.
- Any real implementation on an IS machine MUST be validated with lockout/tagout,
  dry-run, reduced speed and customer safety procedure.
"""


def generate_report(
    config: ProjectConfiguration,
    result: TrajectoryResult,
    filepath: str,
) -> str:
    """
    Generate a Markdown engineering report.

    Args:
        config: Project configuration
        result: Trajectory result
        filepath: Output file path

    Returns:
        Absolute path to the created file.
    """
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    lines = []
    lines.append(f"# RobotSwabbing Engineering Report")
    lines.append(f"")
    lines.append(f"**Project:** {config.project_name}")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Feasible:** {'YES' if result.feasible else 'NO — REVIEW REQUIRED'}")
    lines.append(f"")

    # Safety warnings
    lines.append(_SAFETY_WARNINGS)
    lines.append("")

    # Mould geometry
    lines.append("## Mould Geometry")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Mould Diameter | {config.mould.mould_diameter_mm:.1f} mm |")
    lines.append(f"| Mould Height | {config.mould.mould_height_mm:.1f} mm |")
    lines.append(f"| Neck Height | {config.mould.neck_height_mm:.1f} mm |")
    lines.append(f"| Mould Top Z | {config.mould.mould_top_z_mm:.1f} mm |")
    lines.append(f"| Mould Center X | {config.mould.mould_center_x_mm:.1f} mm |")
    lines.append(f"| Mould Bottom Z | {config.mould.mould_bottom_z_mm:.1f} mm |")
    lines.append("")

    # Obstacles
    lines.append("## Obstacles")
    lines.append("")
    if config.obstacles:
        lines.append("| Name | Type | X min | X max | Z min | Z max | Clearance |")
        lines.append("|------|------|-------|-------|-------|-------|-----------|")
        for obs in config.obstacles:
            lines.append(
                f"| {obs.name} | {obs.obstacle_type.value} | "
                f"{obs.x_min_mm:.1f} | {obs.x_max_mm:.1f} | "
                f"{obs.z_min_mm:.1f} | {obs.z_max_mm:.1f} | "
                f"{obs.clearance_mm:.1f} mm |"
            )
    else:
        lines.append("No obstacles defined.")
    lines.append("")

    # Robot parameters
    lines.append("## Robot / Swabbing Parameters")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Lance Length | {config.robot_params.lance_length_mm} mm |")
    lines.append(f"| Nozzle Offset | {config.robot_params.nozzle_offset_mm:.1f} mm |")
    lines.append(f"| Spray Cone Angle | {config.robot_params.spray_cone_angle_deg:.1f} deg |")
    lines.append(f"| Target Spray Distance | {config.robot_params.target_spray_distance_mm:.1f} mm |")
    lines.append(f"| Minimum Clearance | {config.robot_params.minimum_clearance_mm:.1f} mm |")
    lines.append(f"| Nominal Speed | {config.robot_params.nominal_speed_mm_s:.1f} mm/s |")
    lines.append(f"| Min Speed | {config.robot_params.min_robot_speed_mm_s:.1f} mm/s |")
    lines.append(f"| Max Speed | {config.robot_params.max_robot_speed_mm_s:.1f} mm/s |")
    lines.append(f"| Valve Delay | {config.robot_params.valve_delay_ms:.1f} ms |")
    lines.append(f"| Coating Target | {config.robot_params.coating_target_relative:.2f} |")
    lines.append("")

    # Trajectory
    lines.append("## Calculated Trajectory")
    lines.append("")
    lines.append(f"Total points: {result.total_points}")
    lines.append(f"Min clearance margin: {_fmt_margin(result.min_clearance_margin_mm)}")
    lines.append("")

    lines.append("| ID | X [mm] | Z [mm] | Speed [mm/s] | Valve | Segment | Collision | Margin [mm] | Note |")
    lines.append("|----|--------|--------|-------------|-------|---------|----------|-------------|------|")
    for p in result.points:
        margin_str = _fmt_margin(p.clearance_margin_mm)
        lines.append(
            f"| {p.point_id} | {p.x_mm:.1f} | {p.z_mm:.1f} | "
            f"{p.speed_mm_s:.1f} | {p.valve_state.value} | "
            f"{p.segment_type.value} | {p.collision_status.value} | "
            f"{margin_str} | {p.note} |"
        )
    lines.append("")

    # Collision warnings
    lines.append("## Collision Warnings")
    lines.append("")
    if result.collision_warnings:
        for w in result.collision_warnings:
            lines.append(f"- {w}")
    else:
        lines.append("No collision warnings.")
    lines.append("")

    # Validation checklist
    lines.append("## Validation Checklist")
    lines.append("")
    lines.append("- [ ] Trajectory reviewed by automation engineer")
    lines.append("- [ ] Obstacle geometry verified against machine drawings")
    lines.append("- [ ] Safety clearances confirmed by mechanical engineer")
    lines.append("- [ ] Robot reachability verified (FANUC Robot Simulation / ROBOGUIDE)")
    lines.append("- [ ] Dry-run executed at reduced speed")
    lines.append("- [ ] Lockout/Tagout procedure followed")
    lines.append("- [ ] Customer safety procedure applied")
    lines.append("- [ ] Coating thickness measured and verified")
    lines.append("- [ ] Valve timing verified on machine")
    lines.append("- [ ] Final sign-off by responsible engineer")
    lines.append("")

    report_text = "\n".join(lines)

    with open(filepath, "w") as f:
        f.write(report_text)

    return filepath


def _fmt_margin(margin: float) -> str:
    """Format a clearance margin value."""
    if margin == float("inf") or margin == float("-inf"):
        return "inf"
    return f"{margin:.2f}"
