"""
RobotSimulator — Visualization (3D)

Generates 3D plots showing mould, obstacles,
and the calculated swabbing trajectory using matplotlib.

Provides both 3D views and 2D projections (X-Z, X-Y, Y-Z).
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/headless
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure

# Plotly for interactive 3D
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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


def create_trajectory_plot_3d(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    result: TrajectoryResult,
    global_clearance_mm: float = 0.0,
    title: str = "FANUC Robot Swabbing Trajectory — 3D View",
    figsize: Tuple[float, float] = (14, 12),
    elevation: float = 20.0,
    azimuth: float = 45.0,
) -> Figure:
    """
    Create a complete 3D technical plot of the swabbing trajectory.

    Shows:
    - Mould envelope (3D cylinder)
    - Obstacles (3D boxes with expanded clearance zones)
    - Calculated trajectory with color-coded collision status
    - Valve ON/OFF indication

    Args:
        mould: Mould geometry
        obstacles: List of obstacles
        result: Calculated trajectory result
        global_clearance_mm: Global clearance for obstacle expansion
        title: Plot title
        figsize: Figure size in inches
        elevation: 3D view elevation angle
        azimuth: 3D view azimuth angle

    Returns:
        matplotlib Figure object.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(COLORS["background"])
    fig.patch.set_facecolor(COLORS["background"])

    # Draw mould
    _draw_mould_3d(ax, mould)

    # Draw obstacles
    _draw_obstacles_3d(ax, obstacles, global_clearance_mm)

    # Draw trajectory
    _draw_trajectory_3d(ax, result)

    # Axis labels
    ax.set_xlabel("X position [mm]", fontsize=11)
    ax.set_ylabel("Y position [mm]", fontsize=11)
    ax.set_zlabel("Z position [mm]", fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold")

    # Set view angle
    ax.view_init(elev=elevation, azim=azimuth)

    # Add legend proxies
    _add_3d_legend(ax)

    # Add safety warning
    ax.text2D(
        0.01, 0.01,
        "WARNING: Engineering tool only — validate with robot simulation before use",
        transform=ax.transAxes,
        fontsize=7,
        color="red",
        alpha=0.8,
    )

    plt.tight_layout()
    return fig


def create_trajectory_plot_3d_interactive(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    result: TrajectoryResult,
    global_clearance_mm: float = 0.0,
    title: str = "FANUC Robot Swabbing Trajectory — 3D View (Interactive)",
) -> "go.Figure":
    """
    Create an interactive 3D plot using Plotly.
    
    Supports pan, tilt (rotate), and zoom natively in the browser.
    
    Args:
        mould: Mould geometry
        obstacles: List of obstacles
        result: Calculated trajectory result
        global_clearance_mm: Global clearance for obstacle expansion
        title: Plot title
        
    Returns:
        plotly.graph_objects.Figure with interactive 3D visualization.
        
    Raises:
        ImportError: If plotly is not installed.
    """
    if not PLOTLY_AVAILABLE:
        raise ImportError(
            "Plotly is required for interactive 3D plots. "
            "Install with: pip install plotly"
        )
    
    fig = go.Figure()
    
    # === Draw mould as cylinder ===
    z_bottom = mould.mould_bottom_z_mm
    z_top = mould.mould_top_z_mm
    radius = mould.mould_radius_mm
    x_center = mould.mould_center_x_mm
    y_center = mould.mould_center_y_mm
    
    # Cylinder surface (use fewer points for performance)
    z_cyl = np.linspace(z_bottom, z_top, 30)
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z_cyl)
    x_grid = x_center + radius * np.cos(theta_grid)
    y_grid = y_center + radius * np.sin(theta_grid)
    
    fig.add_trace(go.Surface(
        x=x_grid, y=y_grid, z=z_grid,
        colorscale=[[0, COLORS["mould_fill"]], [1, COLORS["mould_fill"]]],
        opacity=0.3,
        showscale=False,
        name="Mould cavity",
        hoverinfo="skip",
    ))
    
    # Top and bottom edges
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    x_circle = x_center + radius * np.cos(theta_circle)
    y_circle = y_center + radius * np.sin(theta_circle)
    
    fig.add_trace(go.Scatter3d(
        x=x_circle, y=y_circle, z=np.full_like(theta_circle, z_top),
        mode='lines', line=dict(color=COLORS["mould_edge"], width=4),
        name="Mould top", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter3d(
        x=x_circle, y=y_circle, z=np.full_like(theta_circle, z_bottom),
        mode='lines', line=dict(color=COLORS["mould_edge"], width=2, dash='dash'),
        name="Mould bottom", hoverinfo="skip",
    ))
    
    # === Draw obstacles ===
    for obs in obstacles:
        # Expanded box
        x_exp = [
            obs.expanded_x_min_mm - global_clearance_mm,
            obs.expanded_x_max_mm + global_clearance_mm,
        ]
        y_exp = [
            obs.expanded_y_min_mm - global_clearance_mm,
            obs.expanded_y_max_mm + global_clearance_mm,
        ]
        z_exp = [
            obs.expanded_z_min_mm - global_clearance_mm,
            obs.expanded_z_max_mm + global_clearance_mm,
        ]
        _add_box_edges_plotly(fig, x_exp, y_exp, z_exp,
                              color=COLORS["obstacle_expanded"],
                              width=2, dash='dash', opacity=0.3,
                              name=f"{obs.name} (expanded)")
        
        # Original box
        x_orig = [obs.x_min_mm, obs.x_max_mm]
        y_orig = [obs.y_min_mm, obs.y_max_mm]
        z_orig = [obs.z_min_mm, obs.z_max_mm]
        _add_box_edges_plotly(fig, x_orig, y_orig, z_orig,
                              color=COLORS["obstacle_edge"],
                              width=4, dash='solid', opacity=0.8,
                              name=f"{obs.name}")
        
        # Label
        fig.add_trace(go.Scatter3d(
            x=[obs.center_x_mm], y=[obs.center_y_mm], z=[obs.center_z_mm],
            mode='text', text=[obs.name],
            textfont=dict(size=10, color='white', family='Arial Black'),
            showlegend=False, hoverinfo="skip",
        ))
    
    # === Draw trajectory ===
    if result.points:
        xs = [p.x_mm for p in result.points]
        ys = [p.y_mm for p in result.points]
        zs = [p.z_mm for p in result.points]
        
        # Trajectory line
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines', line=dict(color=COLORS["trajectory_line"], width=4),
            name="Trajectory", hoverinfo="skip",
        ))
        
        # Points by collision status
        for status, color, marker, size, name in [
            (CollisionStatus.COLLISION, COLORS["trajectory_collision"], 'x', 6, "Collision"),
            (CollisionStatus.WARNING, COLORS["trajectory_warning"], 'diamond', 5, "Warning"),
        ]:
            pts = [p for p in result.points if p.collision_status == status]
            if pts:
                fig.add_trace(go.Scatter3d(
                    x=[p.x_mm for p in pts], y=[p.y_mm for p in pts], z=[p.z_mm for p in pts],
                    mode='markers',
                    marker=dict(symbol=marker, color=color, size=size, line=dict(width=1, color='white')),
                    name=name, hoverinfo="text",
                    hovertext=[f"{p.segment_type.value} Z={p.z_mm:.1f}" for p in pts],
                ))
        
        # Clear points by segment type
        for seg_type in SegmentType:
            pts = [p for p in result.points 
                   if p.collision_status == CollisionStatus.CLEAR and p.segment_type == seg_type]
            if pts:
                color = _get_segment_color(seg_type)
                marker = _get_segment_marker_plotly(seg_type)
                fig.add_trace(go.Scatter3d(
                    x=[p.x_mm for p in pts], y=[p.y_mm for p in pts], z=[p.z_mm for p in pts],
                    mode='markers',
                    marker=dict(symbol=marker, color=color, size=4, line=dict(width=1, color='white')),
                    name=seg_type.value, hoverinfo="text",
                    hovertext=[f"Z={p.z_mm:.1f}" for p in pts],
                ))
        
        # Valve ON zones
        valve_on = [p for p in result.points if p.valve_state == ValveState.ON]
        if valve_on:
            fig.add_trace(go.Scatter3d(
                x=[p.x_mm for p in valve_on], y=[p.y_mm for p in valve_on], z=[p.z_mm for p in valve_on],
                mode='lines', line=dict(color=COLORS["valve_on"], width=8),
                name="Valve ON", opacity=0.5, hoverinfo="skip",
            ))
    
    # === Layout ===
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        scene=dict(
            xaxis=dict(title="X [mm]", showgrid=True, gridcolor=COLORS["grid"]),
            yaxis=dict(title="Y [mm]", showgrid=True, gridcolor=COLORS["grid"]),
            zaxis=dict(title="Z [mm]", showgrid=True, gridcolor=COLORS["grid"]),
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        ),
        legend=dict(
            x=0.01, y=0.99,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray', borderwidth=1,
            font=dict(size=10),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=True,
    )
    
    # Add safety warning annotation
    fig.add_annotation(
        x=0.01, y=0.01, xref="paper", yref="paper",
        text="⚠️ Engineering tool only — validate with robot simulation before use",
        showarrow=False, font=dict(size=10, color="red"),
        bgcolor="rgba(255,255,255,0.8)", bordercolor="red", borderwidth=1,
    )
    
    return fig


def _add_box_edges_plotly(fig, x, y, z, color, width=2, dash='solid', opacity=1.0, name=None):
    """Add 12 edges of a 3D box to a Plotly figure."""
    x_min, x_max = x
    y_min, y_max = y
    z_min, z_max = z
    
    edges = [
        # Bottom face
        [(x_min, y_min, z_min), (x_max, y_min, z_min)],
        [(x_max, y_min, z_min), (x_max, y_max, z_min)],
        [(x_max, y_max, z_min), (x_min, y_max, z_min)],
        [(x_min, y_max, z_min), (x_min, y_min, z_min)],
        # Top face
        [(x_min, y_min, z_max), (x_max, y_min, z_max)],
        [(x_max, y_min, z_max), (x_max, y_max, z_max)],
        [(x_max, y_max, z_max), (x_min, y_max, z_max)],
        [(x_min, y_max, z_max), (x_min, y_min, z_max)],
        # Vertical
        [(x_min, y_min, z_min), (x_min, y_min, z_max)],
        [(x_max, y_min, z_min), (x_max, y_min, z_max)],
        [(x_max, y_max, z_min), (x_max, y_max, z_max)],
        [(x_min, y_max, z_min), (x_min, y_max, z_max)],
    ]
    
    for edge in edges:
        xs = [p[0] for p in edge]
        ys = [p[1] for p in edge]
        zs = [p[2] for p in edge]
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines', line=dict(color=color, width=width, dash=dash),
            opacity=opacity, name=name, showlegend=False, hoverinfo="skip",
        ))
    # Only show legend for first edge
    if name:
        fig.data[-1].showlegend = True
        fig.data[-1].name = name


def _get_segment_marker_plotly(segment: SegmentType) -> str:
    """Get Plotly marker symbol for a segment type."""
    marker_map = {
        SegmentType.WAIT: 'square',
        SegmentType.APPROACH: 'triangle-up',
        SegmentType.ENTER: 'diamond',
        SegmentType.SWAB_DOWN: 'circle',
        SegmentType.SWAB_UP: 'circle',
        SegmentType.EXIT: 'triangle-down',
    }
    return marker_map.get(segment, 'circle')


def create_projection_plots(
    mould: MouldGeometry,
    obstacles: List[ObstacleEnvelope],
    result: TrajectoryResult,
    global_clearance_mm: float = 0.0,
    title: str = "FANUC Robot Swabbing Trajectory — 2D Projections",
    figsize: Tuple[float, float] = (16, 12),
) -> Figure:
    """
    Create 2D projection plots (X-Z, X-Y, Y-Z views).

    Shows three orthogonal projections for detailed inspection.

    Args:
        mould: Mould geometry
        obstacles: List of obstacles
        result: Trajectory result
        global_clearance_mm: Global clearance
        title: Plot title
        figsize: Figure size

    Returns:
        matplotlib Figure with 3 subplots.
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    fig.patch.set_facecolor(COLORS["background"])

    # X-Z projection (front view)
    ax_xz = axes[0]
    _draw_projection_xz(ax_xz, mould, obstacles, result, global_clearance_mm)
    ax_xz.set_title("Front View (X-Z Plane)", fontsize=12, fontweight="bold")

    # X-Y projection (top view)
    ax_xy = axes[1]
    _draw_projection_xy(ax_xy, mould, obstacles, result, global_clearance_mm)
    ax_xy.set_title("Top View (X-Y Plane)", fontsize=12, fontweight="bold")

    # Y-Z projection (side view)
    ax_yz = axes[2]
    _draw_projection_yz(ax_yz, mould, obstacles, result, global_clearance_mm)
    ax_yz.set_title("Side View (Y-Z Plane)", fontsize=12, fontweight="bold")

    plt.suptitle(title, fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    return fig


def _draw_mould_3d(ax, mould: MouldGeometry):
    """Draw the mould as a 3D cylinder."""
    # Create cylinder for mould cavity
    z_bottom = mould.mould_bottom_z_mm
    z_top = mould.mould_top_z_mm
    radius = mould.mould_radius_mm
    x_center = mould.mould_center_x_mm
    y_center = mould.mould_center_y_mm

    # Create cylinder mesh
    z = np.linspace(z_bottom, z_top, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = x_center + radius * np.cos(theta_grid)
    y_grid = y_center + radius * np.sin(theta_grid)

    # Plot cylinder surface
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color=COLORS["mould_fill"],
                    edgecolor=COLORS["mould_edge"], linewidth=0.5)

    # Draw top and bottom circles
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    x_circle = x_center + radius * np.cos(theta_circle)
    y_circle = y_center + radius * np.sin(theta_circle)

    # Top edge
    ax.plot(x_circle, y_circle, np.full_like(theta_circle, z_top),
            color=COLORS["mould_edge"], linewidth=2, label="Mould top edge")
    # Bottom edge
    ax.plot(x_circle, y_circle, np.full_like(theta_circle, z_bottom),
            color=COLORS["mould_edge"], linewidth=1, linestyle='--')


def _draw_obstacles_3d(ax, obstacles: List[ObstacleEnvelope], global_clearance_mm: float):
    """Draw obstacles as 3D boxes."""
    for i, obs in enumerate(obstacles):
        # Expanded box
        x = [obs.expanded_x_min_mm - global_clearance_mm,
             obs.expanded_x_max_mm + global_clearance_mm]
        y = [obs.expanded_y_min_mm - global_clearance_mm,
             obs.expanded_y_max_mm + global_clearance_mm]
        z = [obs.expanded_z_min_mm - global_clearance_mm,
             obs.expanded_z_max_mm + global_clearance_mm]

        # Draw expanded edges
        _draw_box_edges(ax, x, y, z, color=COLORS["obstacle_expanded"],
                        linewidth=0.5, alpha=0.2, linestyle='--')

        # Original box
        x = [obs.x_min_mm, obs.x_max_mm]
        y = [obs.y_min_mm, obs.y_max_mm]
        z = [obs.z_min_mm, obs.z_max_mm]

        # Draw original edges
        _draw_box_edges(ax, x, y, z, color=COLORS["obstacle_edge"],
                        linewidth=1.5, alpha=0.6)

        # Label
        cx = obs.center_x_mm
        cy = obs.center_y_mm
        cz = obs.center_z_mm
        ax.text(cx, cy, cz, obs.name, fontsize=7, ha='center', va='center',
                fontweight='bold', color='white')


def _draw_box_edges(ax, x, y, z, color, linewidth=1, alpha=1.0, linestyle='-'):
    """Draw the 12 edges of a 3D box."""
    x_min, x_max = x
    y_min, y_max = y
    z_min, z_max = z

    # Bottom face
    bottom_edges = [
        [(x_min, y_min, z_min), (x_max, y_min, z_min)],
        [(x_max, y_min, z_min), (x_max, y_max, z_min)],
        [(x_max, y_max, z_min), (x_min, y_max, z_min)],
        [(x_min, y_max, z_min), (x_min, y_min, z_min)],
    ]
    # Top face
    top_edges = [
        [(x_min, y_min, z_max), (x_max, y_min, z_max)],
        [(x_max, y_min, z_max), (x_max, y_max, z_max)],
        [(x_max, y_max, z_max), (x_min, y_max, z_max)],
        [(x_min, y_max, z_max), (x_min, y_min, z_max)],
    ]
    # Vertical edges
    vertical_edges = [
        [(x_min, y_min, z_min), (x_min, y_min, z_max)],
        [(x_max, y_min, z_min), (x_max, y_min, z_max)],
        [(x_max, y_max, z_min), (x_max, y_max, z_max)],
        [(x_min, y_max, z_min), (x_min, y_max, z_max)],
    ]

    all_edges = bottom_edges + top_edges + vertical_edges
    for edge in all_edges:
        xs = [p[0] for p in edge]
        ys = [p[1] for p in edge]
        zs = [p[2] for p in edge]
        ax.plot(xs, ys, zs, color=color, linewidth=linewidth,
                alpha=alpha, linestyle=linestyle)


def _draw_trajectory_3d(ax, result: TrajectoryResult):
    """Draw the 3D trajectory with color-coded collision status."""
    if not result.points:
        return

    # Draw trajectory line
    xs = [p.x_mm for p in result.points]
    ys = [p.y_mm for p in result.points]
    zs = [p.z_mm for p in result.points]
    ax.plot(xs, ys, zs, color=COLORS["trajectory_line"], linewidth=1.5, alpha=0.7)

    # Draw points with color based on collision status
    for p in result.points:
        if p.collision_status == CollisionStatus.COLLISION:
            color = COLORS["trajectory_collision"]
            marker = "x"
            markersize = 8
        elif p.collision_status == CollisionStatus.WARNING:
            color = COLORS["trajectory_warning"]
            marker = "*"
            markersize = 7
        else:
            color = _get_segment_color(p.segment_type)
            marker = _get_segment_marker(p.segment_type)
            markersize = 6

        ax.plot([p.x_mm], [p.y_mm], [p.z_mm], marker=marker, color=color,
                markersize=markersize, markeredgewidth=1.5)

    # Draw valve ON zones
    valve_on_points = [p for p in result.points if p.valve_state == ValveState.ON]
    if valve_on_points:
        vx = [p.x_mm for p in valve_on_points]
        vy = [p.y_mm for p in valve_on_points]
        vz = [p.z_mm for p in valve_on_points]
        ax.plot(vx, vy, vz, color=COLORS["valve_on"], linewidth=3.0,
                alpha=0.4, label="Valve ON zone")


def _draw_projection_xz(ax, mould, obstacles, result, global_clearance_mm):
    """Draw X-Z projection (front view)."""
    # Draw mould as rectangle
    rect = plt.Rectangle(
        (mould.mould_left_x_mm, mould.mould_bottom_z_mm),
        mould.mould_diameter_mm,
        mould.mould_height_mm,
        linewidth=2, edgecolor=COLORS["mould_edge"],
        facecolor=COLORS["mould_fill"], alpha=0.5, label="Mould"
    )
    ax.add_patch(rect)

    # Draw obstacles as rectangles (projected)
    for obs in obstacles:
        # Expanded
        exp_rect = plt.Rectangle(
            (obs.expanded_x_min_mm - global_clearance_mm,
             obs.expanded_z_min_mm - global_clearance_mm),
            (obs.x_max_mm - obs.x_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            (obs.z_max_mm - obs.z_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            linewidth=0.5, edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_expanded"], alpha=0.2, linestyle='--'
        )
        ax.add_patch(exp_rect)
        # Original
        orig_rect = plt.Rectangle(
            (obs.x_min_mm, obs.z_min_mm),
            obs.width_mm, obs.height_mm,
            linewidth=1.5, edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_original"], alpha=0.5
        )
        ax.add_patch(orig_rect)

    # Draw trajectory projection
    _draw_trajectory_2d(ax, result, x_idx=0, y_idx=2)  # X, Z

    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Z [mm]")
    ax.grid(True, color=COLORS["grid"], linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_aspect('equal')


def _draw_projection_xy(ax, mould, obstacles, result, global_clearance_mm):
    """Draw X-Y projection (top view)."""
    # Draw mould as rectangle/circle
    if mould.mould_depth_mm > 0:
        rect = plt.Rectangle(
            (mould.mould_left_x_mm, mould.mould_front_y_mm),
            mould.mould_diameter_mm,
            mould.effective_y_depth_mm,
            linewidth=2, edgecolor=COLORS["mould_edge"],
            facecolor=COLORS["mould_fill"], alpha=0.5
        )
        ax.add_patch(rect)
    else:
        circle = plt.Circle(
            (mould.mould_center_x_mm, mould.mould_center_y_mm),
            mould.mould_radius_mm,
            linewidth=2, edgecolor=COLORS["mould_edge"],
            facecolor=COLORS["mould_fill"], alpha=0.5
        )
        ax.add_patch(circle)

    # Draw obstacles (projected)
    for obs in obstacles:
        exp_rect = plt.Rectangle(
            (obs.expanded_x_min_mm - global_clearance_mm,
             obs.expanded_y_min_mm - global_clearance_mm),
            (obs.x_max_mm - obs.x_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            (obs.y_max_mm - obs.y_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            linewidth=0.5, edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_expanded"], alpha=0.2, linestyle='--'
        )
        ax.add_patch(exp_rect)
        orig_rect = plt.Rectangle(
            (obs.x_min_mm, obs.y_min_mm),
            obs.width_mm, obs.depth_mm,
            linewidth=1.5, edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_original"], alpha=0.5
        )
        ax.add_patch(orig_rect)

    # Draw trajectory
    _draw_trajectory_2d(ax, result, x_idx=0, y_idx=1)  # X, Y

    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.grid(True, color=COLORS["grid"], linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_aspect('equal')


def _draw_projection_yz(ax, mould, obstacles, result, global_clearance_mm):
    """Draw Y-Z projection (side view)."""
    # Draw mould
    rect = plt.Rectangle(
        (mould.mould_front_y_mm, mould.mould_bottom_z_mm),
        mould.effective_y_depth_mm,
        mould.mould_height_mm,
        linewidth=2, edgecolor=COLORS["mould_edge"],
        facecolor=COLORS["mould_fill"], alpha=0.5
    )
    ax.add_patch(rect)

    # Draw obstacles
    for obs in obstacles:
        exp_rect = plt.Rectangle(
            (obs.expanded_y_min_mm - global_clearance_mm,
             obs.expanded_z_min_mm - global_clearance_mm),
            (obs.y_max_mm - obs.y_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            (obs.z_max_mm - obs.z_min_mm) + 2 * (obs.clearance_mm + global_clearance_mm),
            linewidth=0.5, edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_expanded"], alpha=0.2, linestyle='--'
        )
        ax.add_patch(exp_rect)
        orig_rect = plt.Rectangle(
            (obs.y_min_mm, obs.z_min_mm),
            obs.depth_mm, obs.height_mm,
            linewidth=1.5, edgecolor=COLORS["obstacle_edge"],
            facecolor=COLORS["obstacle_original"], alpha=0.5
        )
        ax.add_patch(orig_rect)

    # Draw trajectory
    _draw_trajectory_2d(ax, result, x_idx=1, y_idx=2)  # Y, Z

    ax.set_xlabel("Y [mm]")
    ax.set_ylabel("Z [mm]")
    ax.grid(True, color=COLORS["grid"], linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_aspect('equal')


def _draw_trajectory_2d(ax, result, x_idx=0, y_idx=1):
    """Draw 2D trajectory projection."""
    if not result.points:
        return

    coords = [(p.x_mm, p.y_mm, p.z_mm) for p in result.points]
    xs = [c[x_idx] for c in coords]
    ys = [c[y_idx] for c in coords]

    # Line
    ax.plot(xs, ys, color=COLORS["trajectory_line"], linewidth=1.2, alpha=0.7)

    # Points
    for p in result.points:
        coord = [p.x_mm, p.y_mm, p.z_mm]
        if p.collision_status == CollisionStatus.COLLISION:
            color = COLORS["trajectory_collision"]
            marker = "x"
        elif p.collision_status == CollisionStatus.WARNING:
            color = COLORS["trajectory_warning"]
            marker = "*"
        else:
            color = _get_segment_color(p.segment_type)
            marker = "o"
        ax.plot(coord[x_idx], coord[y_idx], marker=marker, color=color,
                markersize=5, alpha=0.8)


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
        SegmentType.WAIT: "s",
        SegmentType.APPROACH: "^",
        SegmentType.ENTER: "D",
        SegmentType.SWAB_DOWN: "o",
        SegmentType.SWAB_UP: "o",
        SegmentType.EXIT: "v",
    }
    return marker_map.get(segment, "o")


def _add_3d_legend(ax):
    """Add legend to 3D plot."""
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label='Wait',
               markerfacecolor=COLORS["wait_marker"], markersize=8),
        Line2D([0], [0], marker='^', color='w', label='Approach',
               markerfacecolor=COLORS["trajectory_clear"], markersize=8),
        Line2D([0], [0], marker='D', color='w', label='Entry',
               markerfacecolor=COLORS["entry_marker"], markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Swab',
               markerfacecolor=COLORS["swab_zone"], markersize=8),
        Line2D([0], [0], marker='v', color='w', label='Exit',
               markerfacecolor=COLORS["exit_marker"], markersize=8),
        Line2D([0], [0], marker='x', color='w', label='Collision',
               markerfacecolor='none', markeredgewidth=2, markersize=8),
        Line2D([0], [0], color=COLORS["valve_on"], linewidth=3, label='Valve ON'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8)


def save_plot(fig: Figure, filepath: str, dpi: int = 150) -> str:
    """
    Save a matplotlib figure to file.

    Args:
        fig: The figure to save
        filepath: Output file path
        dpi: Resolution

    Returns:
        Absolute path to saved file.
    """
    import os
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    return filepath