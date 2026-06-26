"""
RobotSimulator — Streamlit Web Application

FANUC Robot Swabbing Trajectory Calculator
for IS Hollow Glass Forming Machine — Blank Side

Run with: streamlit run app.py
"""

from __future__ import annotations

import os
import sys
import json

# Ensure the package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from robotsimulator import (
    VERSION,
    VERSION_STRING,
    BUILD_DATE,
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
    GITHUB_URL,
    LICENSE,
    COPYRIGHT_YEAR,
    COPYRIGHT_HOLDER,
    ENGINEERING_DISCLAIMER,
)
from robotsimulator.models import (
    MouldGeometry,
    ObstacleEnvelope,
    ObstacleType,
    RobotParameters,
    SwabbingParameters,
    TrajectoryResult,
    ProjectConfiguration,
    VALID_LANCE_LENGTHS,
)
from robotsimulator.trajectory import generate_trajectory
from robotsimulator.export import export_csv, export_json, generate_report
from robotsimulator.plotting import create_trajectory_plot, save_plot


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title=f"{PROJECT_NAME} — FANUC Trajectory Calculator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(f"🤖 {PROJECT_NAME}")
st.caption(f"{PROJECT_DESCRIPTION}  |  v{VERSION} — {BUILD_DATE}  |  {LICENSE}")

# Version badge in sidebar — always visible
with st.sidebar:
    st.caption(f"v{VERSION} | {BUILD_DATE}")

# Engineering disclaimer at the top
with st.expander("⚠️ SAFETY DISCLAIMER — Read before use", expanded=False):
    # Render markdown sections by stripping leading/trailing whitespace
    sections = ENGINEERING_DISCLAIMER.split("##")
    for s in sections:
        if s.strip():
            st.markdown("##" + s)

# ============================================================================
# Initialize Session State
# ============================================================================

if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "trajectory_result" not in st.session_state:
    st.session_state.trajectory_result = None
if "config" not in st.session_state:
    st.session_state.config = None


# ============================================================================
# Sidebar — Input Parameters
# ============================================================================

with st.sidebar:
    st.header("⚙️ Parameters")

    # --- Mould Geometry ---
    st.subheader("📐 Mould Geometry")
    mould_diameter = st.number_input(
        "Mould diameter [mm]", min_value=10.0, max_value=500.0,
        value=150.0, step=5.0, help="Inner diameter of the blank mould"
    )
    mould_height = st.number_input(
        "Mould height [mm]", min_value=10.0, max_value=500.0,
        value=120.0, step=5.0, help="Height of the mould cavity"
    )
    neck_height = st.number_input(
        "Neck height [mm]", min_value=0.0, max_value=200.0,
        value=20.0, step=5.0, help="Height of the neck ring below mould"
    )
    mould_top_z = st.number_input(
        "Mould top Z [mm]", value=200.0, step=10.0,
        help="Z coordinate of the mould top edge (upper wire)"
    )
    mould_center_x = st.number_input(
        "Mould center X [mm]", value=0.0, step=10.0,
        help="X coordinate of the mould centerline"
    )

    # --- Lance Selection ---
    st.subheader("🔫 Lance Selection")
    lance_length = st.selectbox(
        "Lance length [mm]",
        options=[200, 250, 300],
        index=1,
        help="Length of the swabbing lance/nozzle assembly"
    )

    # --- Robot Parameters ---
    st.subheader("🤖 Robot Parameters")
    nozzle_offset = st.number_input(
        "Nozzle offset [mm]", min_value=0.0, value=0.0, step=1.0,
        help="Offset from lance tip to spray point"
    )
    spray_cone_angle = st.number_input(
        "Spray cone angle [deg]", min_value=1.0, max_value=90.0,
        value=30.0, step=5.0, help="Half-angle of the spray cone"
    )
    target_spray_dist = st.number_input(
        "Target spray distance [mm]", min_value=1.0,
        value=50.0, step=5.0,
        help="Working distance from nozzle to mould surface"
    )
    min_clearance = st.number_input(
        "Minimum clearance [mm]", min_value=1.0,
        value=10.0, step=1.0,
        help="Minimum safety distance from any obstacle"
    )
    nominal_speed = st.number_input(
        "Nominal speed [mm/s]", min_value=10.0,
        value=200.0, step=10.0,
        help="Robot speed at reference diameter"
    )
    min_speed = st.number_input(
        "Min speed [mm/s]", min_value=1.0,
        value=50.0, step=10.0,
        help="Minimum allowed robot speed"
    )
    max_speed = st.number_input(
        "Max speed [mm/s]", min_value=10.0,
        value=500.0, step=10.0,
        help="Maximum allowed robot speed"
    )
    valve_delay = st.number_input(
        "Valve delay [ms]", min_value=0.0,
        value=50.0, step=10.0,
        help="Valve opening/closing delay in milliseconds"
    )
    coating_target = st.number_input(
        "Coating target (relative)", min_value=0.01, max_value=1.0,
        value=1.0, step=0.05,
        help="Relative coating target (1.0 = full coating)"
    )

    # --- Swabbing Parameters ---
    st.subheader("🔄 Swabbing Process")
    swab_step = st.number_input(
        "Swab step [mm]", min_value=1.0, value=10.0, step=1.0,
        help="Vertical distance between swab points"
    )
    include_swab_up = st.checkbox(
        "Include swab-up pass",
        value=False,
        help="Add a return upward pass with spray active"
    )
    approach_height = st.number_input(
        "Approach height above obstacles [mm]", min_value=10.0,
        value=50.0, step=10.0,
        help="Height above highest obstacle for approach position"
    )
    entry_offset_x = st.number_input(
        "Entry X offset [mm]", value=0.0, step=5.0,
        help="Offset from mould center X for swab path"
    )

    # --- Calculate Button ---
    st.markdown("---")
    calculate_btn = st.button(
        "🚀 Calculate Trajectory",
        type="primary",
        use_container_width=True,
    )


# ============================================================================
# Main Content Area
# ============================================================================

col1, col2 = st.columns([1, 2])

with col1:
    # --- Obstacle Definition ---
    st.subheader("🚧 Obstacle Definition")

    obs_name = st.text_input("Obstacle name", value="", key="obs_name")
    obs_type = st.selectbox(
        "Obstacle type",
        options=[t.value for t in ObstacleType],
        index=0,
        key="obs_type",
    )
    col_obs1, col_obs2 = st.columns(2)
    with col_obs1:
        obs_x_min = st.number_input("X min [mm]", value=-50.0, step=5.0, key="oxmin")
        obs_z_min = st.number_input("Z min [mm]", value=200.0, step=5.0, key="ozmin")
    with col_obs2:
        obs_x_max = st.number_input("X max [mm]", value=50.0, step=5.0, key="oxmax")
        obs_z_max = st.number_input("Z max [mm]", value=230.0, step=5.0, key="ozmax")

    obs_clearance = st.number_input(
        "Obstacle clearance [mm]", min_value=0.0, value=5.0, step=1.0,
        key="obs_clearance",
    )

    if st.button("➕ Add Obstacle", use_container_width=True):
        if obs_name.strip():
            try:
                new_obs = ObstacleEnvelope(
                    name=obs_name.strip(),
                    obstacle_type=ObstacleType(obs_type),
                    x_min_mm=obs_x_min,
                    x_max_mm=obs_x_max,
                    z_min_mm=obs_z_min,
                    z_max_mm=obs_z_max,
                    clearance_mm=obs_clearance,
                )
                st.session_state.obstacles.append(new_obs)
                st.success(f"Obstacle '{obs_name}' added!")
            except ValueError as e:
                st.error(f"Invalid obstacle: {e}")
        else:
            st.error("Obstacle name cannot be empty.")

    if st.button("🗑️ Clear All Obstacles"):
        st.session_state.obstacles = []
        st.info("All obstacles cleared.")

    # Display current obstacles
    if st.session_state.obstacles:
        st.markdown("**Current obstacles:**")
        for i, obs in enumerate(st.session_state.obstacles):
            with st.expander(f"{obs.name} ({obs.obstacle_type.value})", expanded=False):
                st.write(
                    f"X: [{obs.x_min_mm:.1f}, {obs.x_max_mm:.1f}] mm | "
                    f"Z: [{obs.z_min_mm:.1f}, {obs.z_max_mm:.1f}] mm | "
                    f"Clearance: {obs.clearance_mm:.1f} mm"
                )
                if st.button(f"❌ Remove", key=f"remove_obs_{i}"):
                    st.session_state.obstacles.pop(i)
                    st.rerun()

    # --- Load Sample Obstacles ---
    st.markdown("---")
    if st.button("📋 Load sample obstacles (blank side)"):
        st.session_state.obstacles = _get_sample_obstacles()
        st.success("Sample obstacles loaded!")
        st.rerun()


with col2:
    st.subheader("📊 Trajectory Result")

    # --- Calculation ---
    if calculate_btn:
        with st.spinner("Calculating trajectory..."):
            try:
                mould = MouldGeometry(
                    mould_diameter_mm=mould_diameter,
                    mould_height_mm=mould_height,
                    neck_height_mm=neck_height,
                    mould_top_z_mm=mould_top_z,
                    mould_center_x_mm=mould_center_x,
                )

                robot_params = RobotParameters(
                    lance_length_mm=lance_length,
                    nozzle_offset_mm=nozzle_offset,
                    spray_cone_angle_deg=spray_cone_angle,
                    target_spray_distance_mm=target_spray_dist,
                    minimum_clearance_mm=min_clearance,
                    max_robot_speed_mm_s=max_speed,
                    min_robot_speed_mm_s=min_speed,
                    nominal_speed_mm_s=nominal_speed,
                    valve_delay_ms=valve_delay,
                    coating_target_relative=coating_target,
                )

                swabbing_params = SwabbingParameters(
                    reference_diameter_mm=mould_diameter,
                    coating_start_z_mm=mould_top_z,
                    coating_end_z_mm=mould.mould_bottom_z_mm,
                    swab_step_mm=swab_step,
                    include_swab_up=include_swab_up,
                    entry_offset_x_mm=entry_offset_x,
                    approach_height_mm=approach_height,
                )

                result = generate_trajectory(
                    mould=mould,
                    obstacles=st.session_state.obstacles,
                    robot_params=robot_params,
                    swabbing_params=swabbing_params,
                )

                config = ProjectConfiguration(
                    project_name="RobotSwabbing_Session",
                    mould=mould,
                    obstacles=list(st.session_state.obstacles),
                    robot_params=robot_params,
                    swabbing_params=swabbing_params,
                )

                st.session_state.trajectory_result = result
                st.session_state.config = config

            except ValueError as e:
                st.error(f"Input validation error: {e}")
                st.session_state.trajectory_result = None
                st.session_state.config = None

    # --- Display Results ---
    if st.session_state.trajectory_result is not None:
        result = st.session_state.trajectory_result
        config = st.session_state.config

        # Feasibility indicator
        if result.feasible:
            st.success("✅ Trajectory is FEASIBLE — no collisions detected")
        else:
            st.error("❌ Trajectory has COLLISIONS — review obstacle geometry")

        if result.has_warnings:
            st.warning(f"⚠️ {len(result.collision_warnings)} warnings found")

        # Summary metrics
        met_col1, met_col2, met_col3, met_col4 = st.columns(4)
        with met_col1:
            st.metric("Points", result.total_points)
        with met_col2:
            margin = result.min_clearance_margin_mm
            margin_str = f"{margin:.1f}" if margin != float("inf") else "∞"
            st.metric("Min Clearance", f"{margin_str} mm")
        with met_col3:
            swab_pts = [p for p in result.points
                        if p.segment_type.value in ("swab_down", "swab_up")]
            avg_speed = (sum(p.speed_mm_s for p in swab_pts) / len(swab_pts)
                         if swab_pts else 0)
            st.metric("Avg Swab Speed", f"{avg_speed:.1f} mm/s")
        with met_col4:
            on_pts = sum(1 for p in result.points if p.valve_state.value == "ON")
            st.metric("Valve ON Points", on_pts)

        # Collision warnings
        if result.collision_warnings:
            with st.expander("⚠️ Collision Warnings", expanded=True):
                for w in result.collision_warnings:
                    st.warning(w)

        # Trajectory plot
        st.subheader("📈 X-Z Trajectory Plot")
        fig = create_trajectory_plot(
            mould=config.mould,
            obstacles=config.obstacles,
            result=result,
            global_clearance_mm=config.robot_params.minimum_clearance_mm,
        )
        st.pyplot(fig)

        # Trajectory table
        st.subheader("📋 Trajectory Points")
        with st.expander("Show all trajectory points", expanded=True):
            _display_trajectory_table(result)

        # Export buttons
        st.subheader("💾 Export")
        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            if st.button("📄 Export CSV"):
                csv_path = export_csv(result, "outputs/trajectory_export.csv")
                with open(csv_path, "r") as f:
                    st.download_button(
                        "Download CSV",
                        data=f.read(),
                        file_name="trajectory_export.csv",
                        mime="text/csv",
                    )

        with export_col2:
            if st.button("📦 Export JSON"):
                json_path = export_json(config, result, "outputs/trajectory_export.json")
                with open(json_path, "r") as f:
                    st.download_button(
                        "Download JSON",
                        data=f.read(),
                        file_name="trajectory_export.json",
                        mime="application/json",
                    )

        with export_col3:
            if st.button("📝 Generate Report"):
                report_path = generate_report(
                    config, result, "outputs/engineering_report.md"
                )
                with open(report_path, "r") as f:
                    st.download_button(
                        "Download Report",
                        data=f.read(),
                        file_name="engineering_report.md",
                        mime="text/markdown",
                    )
    else:
        st.info("Set parameters in the sidebar and click **Calculate Trajectory** to begin.")


# ============================================================================
# Helper Functions
# ============================================================================

def _display_trajectory_table(result: TrajectoryResult):
    """Display trajectory points as a Streamlit dataframe."""
    import pandas as pd

    rows = []
    for p in result.points:
        margin_str = (
            f"{p.clearance_margin_mm:.2f}" if p.clearance_margin_mm != float("inf")
            else "inf"
        )
        rows.append({
            "ID": p.point_id,
            "X [mm]": round(p.x_mm, 1),
            "Z [mm]": round(p.z_mm, 1),
            "Speed [mm/s]": round(p.speed_mm_s, 1),
            "Valve": p.valve_state.value,
            "Segment": p.segment_type.value,
            "Collision": p.collision_status.value,
            "Margin [mm]": margin_str,
            "Note": p.note,
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=300)


def _get_sample_obstacles():
    """Return sample obstacles for a typical IS machine blank side."""
    return [
        ObstacleEnvelope(
            name="Upper Wire / Mould Edge",
            obstacle_type=ObstacleType.MOULD_UPPER_EDGE,
            x_min_mm=-80.0,
            x_max_mm=80.0,
            z_min_mm=195.0,
            z_max_mm=205.0,
            clearance_mm=5.0,
        ),
        ObstacleEnvelope(
            name="Deflector",
            obstacle_type=ObstacleType.DEFLECTOR,
            x_min_mm=-100.0,
            x_max_mm=100.0,
            z_min_mm=210.0,
            z_max_mm=240.0,
            clearance_mm=8.0,
        ),
        ObstacleEnvelope(
            name="Baffle Mechanism",
            obstacle_type=ObstacleType.BAFFLE_MECHANISM,
            x_min_mm=-120.0,
            x_max_mm=-40.0,
            z_min_mm=160.0,
            z_max_mm=260.0,
            clearance_mm=5.0,
        ),
        ObstacleEnvelope(
            name="Funnel Mechanism",
            obstacle_type=ObstacleType.FUNNEL_MECHANISM,
            x_min_mm=40.0,
            x_max_mm=120.0,
            z_min_mm=160.0,
            z_max_mm=260.0,
            clearance_mm=5.0,
        ),
    ]


# ============================================================================
# Footer
# ============================================================================

st.markdown("---")
st.caption(
    f"{PROJECT_NAME} v{VERSION} — {BUILD_DATE}  |  "
    f"{PROJECT_DESCRIPTION}  |  "
    f"Engineering Tool Only  |  "
    f"[GitHub]({GITHUB_URL})"
)
