"""
RobotSimulator — Visualization

Generates technical X-Z plots showing mould, obstacles,
and the calculated swabbing trajectory using matplotlib.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/headless
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure

from .models import (
    MouldGeometry,
    ObstacleEnvelope,
    ObstacleType,
    TrajectoryResult,
    TrajectoryPoint,
    CollisionStatus,
    ValveState,
    SegmentType,
)


# ============================================================================
# Color scheme — technical engineering style
# ============================================================================

COLORS = {
    "mould_fill": "#D4E6F1",       # Light blue
    "mould_edge": "#2C3E50",       # Dark blue
    "neck_fill": "#FADBD8",        # Light red/pink
    "neck_edge": "#922B21",        # Dark red
    "obstacle_expanded": "#F5B7B1", # Light red (expanded zone)
    "obstacle_original": "#E74C3C", # Red (actual obstacle)
    "obstacle_edge": "#922B21",     # Dark red edge
    "trajectory_clear": "#2ECC71",  # Green
    "trajectory_warning": "#F39C12", # Orange
    "trajectory_collision": "#E74C3C", # Red
    "trajectory_line": "#2980B9",   # Blue
    "valve_on": "#27AE60",         # Green
    "valve_off": "#95A5A6",        # Grey
    "wait_marker": "#8E44AD",      # Purple
    "entry_marker": "#2980B9",     # Blue
    "swab_zone": "#2ECC71",        # Green
    "exit_marker": "#E67E22",      # Orange
    "background": "#FFFFFF",
    "grid": "#E5E8E8",
}


def create_trajectory_plot(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    result: TrajectoryResult,
    global_clearance_mm: float = 0.0,
    title: str = "FANUC Robot Swabbing Trajectory — Blank Side IS Machine",
    figsize: Tuple[float, float] = (12, 10),
) -> Figure:
    """
    Create a complete X-Z technical plot of the swabbing trajectory.

    Shows:
    - Mould envelope (cavity + neck)
    - Mould centerline
    - Obstacles (original + expanded with clearance)
    - Calculated trajectory with color-coded collision status
    - Valve ON/OFF indication
    - Wait, Entry, Swab, Exit markers

    Args:
        mould: Mould geometry
        obstacles: List of obstacles
        result: Calculated trajectory result
        global_clearance_mm: Global clearance for obstacle expansion
        title: Plot title
        figsize: Figure size in inches

    Returns:
        matplotlib Figure object.
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # Set background
    fig.patch.set_facecolor(COLORS["background"])
    ax.set_facecolor(COLORS["background"])

    # Draw mould cavity
    _draw_mould(ax, mould)

    # Draw obstacles
    _draw_obstacles(ax, obstacles, global_clearance_mm)

    # Draw trajectory
    _draw_trajectory(ax, result)

    # Draw mould centerline
    ax.axvline(
        x=mould.mould_center_x_mm,
        color=COLORS["mould_edge"],
        linestyle="--",
        linewidth=0.8,
        alpha=0.5,
        label="Mould centerline",
    )

    # Axis labels and formatting
    ax.set_xlabel("X position [mm]", fontsize=12)
    ax.set_ylabel("Z position [mm]", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")

    # Add legend
    ax.legend(loc="upper right", fontsize=8, framealpha=0.9)

    # Grid
    ax.grid(True, color=COLORS["grid"], linestyle="-", linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)

    # Set reasonable axis limits
    _set_axis_limits(ax, mould, obstacles, result)

    # Add safety warning text
    ax.text(
        0.01, 0.01,
        "WARNING: Engineering tool only — validate with robot simulation before use",
        transform=ax.transAxes,
        fontsize=7,
        color="red",
        alpha=0.8,
        verticalalignment="bottom",
    )

    plt.tight_layout()
    return fig


def _draw_mould(ax, mould: MouldGeometry):
    """Draw the mould cavity and neck on the plot."""
    # Mould cavity
    mould_rect = patches.Rectangle(
        (mould.mould_left_x_mm, mould.mould_bottom_z_mm),
        mould.mould_diameter_mm,
        mould.mould_height_mm,
        linewidth=2,
        edgecolor=COLORS["mould_edge"],
        facecolor=COLORS["mould_fill"],
        label="Mould cavity",
    )
    ax.add_patch(mould_rect)

    # Neck ring (below mould)
    if mould.neck_height_mm > 0:
        neck_rect = patches.Rectangle(
            (mould.mould_center_x_mm - mould.mould_diameter_mm * 0.4,
             mould.neck_bottom_z_mm),
            mould.mould_diameter_mm * 0.8,
            mould.neck_height_mm,
            linewidth=1.5,
            edgecolor=COLORS["neck_edge"],
            facecolor=COLORS["neck_fill"],
            label="Neck ring",
        )
        ax.add_patch(neck_rect)

    # Mould top edge marker (upper wire)
    ax.plot(
        [mould.mould_left_x_mm - 5, mould.mould_right_x_mm + 5],
        [mould.mould_top_z_mm, mould.mould_top_z_mm],
        color=COLORS["mould_edge"],
        linewidth=1.5,
        linestyle="-",
        alpha=0.7,
        label="Upper wire",
    )

    # Mould bottom marker
    ax.plot(
        [mould.mould_left_x_mm - 5, mould.mould_right_x_mm + 5],
        [mould.mould_bottom_z_mm, mould.mould_bottom_z_mm],
        color=COLORS["neck_edge"],
        linewidth=1.0,
        linestyle=":",
        alpha=0.5,
    )


def _draw_obstacles(ax, obstacles: List[ObstacleEnvelope], global_clearance_mm: float):
    """Draw obstacles with their expanded clearance zones."""
    for i, obs in enumerate(obstacles):
        # Expanded envelope (with clearance)
        expanded_rect = patches.Rectangle(
            (obs.expanded_x_min_mm - global_clearance_mm,
             obs.expanded_z_min_mm - global_clearance_mm),
            (obs.x_max_mm - obs.x_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            (obs.z_max_mm - obs.z_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            linewidth=0.5,
            edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_expanded"],
            alpha=0.3,
            linestyle="--",
            label="Expanded zone" if i == 0 else "",
        )
        ax.add_patch(expanded_rect)

        # Original obstacle
        orig_rect = patches.Rectangle(
            (obs.x_min_mm, obs.z_min_mm),
            obs.x_max_mm - obs.x_min_mm,
            obs.z_max_mm - obs.z_min_mm,
            linewidth=1.5,
            edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_original"],
            alpha=0.6,
            label="Obstacle" if i == 0 else "",
        )
        ax.add_patch(orig_rect)

        # Label
        ax.text(
            obs.center_x_mm,
            obs.center_z_mm,
            obs.name,
            fontsize=7,
            ha="center",
            va="center",
            fontweight="bold",
            color="white",
        )


def _draw_trajectory(ax, result: TrajectoryResult):
    """Draw the swabbing trajectory with color-coded collision status and markers."""
    if not result.points:
        return

    # Draw trajectory line
    xs = [p.x_mm for p in result.points]
    zs = [p.z_mm for p in result.points]
    ax.plot(xs, zs, color=COLORS["trajectory_line"], linewidth=1.2, alpha=0.7)

    # Draw each point with color based on collision status
    for p in result.points:
        if p.collision_status == CollisionStatus.COLLISION:
            color = COLORS["trajectory_collision"]
            marker = "x"
            markersize = 8
        elif p.collision_status == CollisionStatus.WARNING:
            color = COLORS["trajectory_warning"]
            marker = "!"
            markersize = 7
        else:
            # Color based on segment type
            color = _get_segment_color(p.segment_type)
            marker = _get_segment_marker(p.segment_type)
            markersize = 6

        ax.plot(p.x_mm, p.z_mm, marker=marker, color=color,
                markersize=markersize, markeredgewidth=1.5)

    # Draw valve ON/OFF zones
    valve_on_points = [p for p in result.points if p.valve_state == ValveState.ON]
    if valve_on_points:
        vx = [p.x_mm for p in valve_on_points]
        vz = [p.z_mm for p in valve_on_points]
        ax.plot(vx, vz, color=COLORS["valve_on"], linewidth=3.0,
                alpha=0.4, label="Valve ON zone", solid_capstyle="round")

    # Add point ID labels for key points (first, entry, swab start/end, exit, last)
    key_points = []
    for p in result.points:
        if p.segment_type in (SegmentType.WAIT, SegmentType.ENTER, SegmentType.EXIT):
            key_points.append(p)

    # Also label first and last swab points
    swab_points = [p for p in result.points
                   if p.segment_type in (SegmentType.SWAB_DOWN, SegmentType.SWAB_UP)]
    if swab_points:
        key_points.append(swab_points[0])
        key_points.append(swab_points[-1])

    for p in key_points:
        ax.annotate(
            f"P{p.point_id}",
            (p.x_mm, p.z_mm),
            textcoords="offset points",
            xytext=(8, 5),
            fontsize=7,
            color=COLORS["mould_edge"],
            fontweight="bold",
        )


def _get_segment_color(segment: SegmentType) -> str:
    """Get color for a trajectory segment type."""
    color_map = {
        SegmentType.WAIT: COLORS["wait_marker"],
        SegmentType.APPROACH: COLORS["trajectory_clear"],
        SegmentType.ENTER: COLORS["entry_marker"],
        SegmentType.SWAB_DOWN: COLORS["swab_zone"],
        SegmentType.SWAB_UP: "#16A085",
        SegmentType.EXIT: COLORS["exit_marker"],
    }
    return color_map.get(segment, COLORS["trajectory_clear"])


def _get_segment_marker(segment: SegmentType) -> str:
    """Get marker style for a segment type."""
    marker_map = {
        SegmentType.WAIT: "s",      # Square
        SegmentType.APPROACH: "^",  # Triangle up
        SegmentType.ENTER: "D",    # Diamond
        SegmentType.SWAB_DOWN: "o", # Circle
        SegmentType.SWAB_UP: "o",  # Circle
        SegmentType.EXIT: "v",     # Triangle down
    }
    return marker_map.get(segment, "o")


def _set_axis_limits(ax, mould, obstacles, result):
    """Set reasonable axis limits based on geometry and trajectory."""
    all_x = [mould.mould_left_x_mm, mould.mould_right_x_mm]
    all_z = [mould.neck_bottom_z_mm, mould.mould_top_z_mm]

    for obs in obstacles:
        all_x.extend([obs.expanded_x_min_mm, obs.expanded_x_max_mm])
        all_z.extend([obs.expanded_z_min_mm, obs.expanded_z_max_mm])

    for p in result.points:
        all_x.append(p.x_mm)
        all_z.append(p.z_mm)

    x_min, x_max = min(all_x), max(all_x)
    z_min, z_max = min(all_z), max(all_z)

    # Add 20% margin
    x_margin = max(20.0, (x_max - x_min) * 0.2)
    z_margin = max(20.0, (z_max - z_min) * 0.1)

    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(z_min - z_margin, z_max + z_margin)

    # Equal aspect for proper geometry visualization
    ax.set_aspect("equal", adjustable="datalim")


def save_plot(fig: Figure, filepath: str, dpi: int = 150) -> str:
    """
    Save a matplotlib figure to file.

    Args:
        fig: The figure to save
        filepath: Output file path (PNG recommended)
        dpi: Resolution in dots per inch

    Returns:
        Absolute path to the saved file.
    """
    import os
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    return filepath
