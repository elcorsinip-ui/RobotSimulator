"""
RobotSimulator — Streamlit Web Application (3D)
FANUC Robot Swabbing Trajectory Calculator for IS Machine — 3D Version
Run with: streamlit run app.py

Version 0.3.3: Obstacle type colors in 3D (DEFLECTOR=cyan, MOULD=brown, etc.),
semi-transparent face fills, enhanced labels with type info.
Obstacle edit/remove UI, default deflector obstacle, DEFLECTOR excluded from wait Z.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from robotsimulator import VERSION, VERSION_STRING, BUILD_DATE, PROJECT_NAME, PROJECT_DESCRIPTION, LICENSE, ENGINEERING_DISCLAIMER
from robotsimulator.models import MouldGeometry, ObstacleEnvelope, ObstacleType, RobotParameters, SwabbingParameters, ProjectConfiguration, VALID_LANCE_LENGTHS
from robotsimulator.trajectory import generate_trajectory
from robotsimulator.export import export_csv, export_json, generate_report
from robotsimulator.plotting import create_trajectory_plot_3d, create_trajectory_plot_3d_interactive, create_projection_plots, save_plot

st.set_page_config(page_title=f"{PROJECT_NAME} (3D)", page_icon="🤖", layout="wide")
st.title(f"🤖 {PROJECT_NAME} (3D)")
st.caption(f"{PROJECT_DESCRIPTION} (3D) | v{VERSION} — {BUILD_DATE} | {LICENSE}")

with st.sidebar:
    st.caption(f"v{VERSION} | {BUILD_DATE}")
    st.header("⚙️ Parameters")
    st.subheader("📐 Mould (3D)")
    mould_diameter = st.number_input("Diameter [mm]", 10.0, 500.0, 60.0, 5.0)
    mould_height = st.number_input("Height [mm]", 10.0, 500.0, 250.0, 5.0)
    mould_depth = st.number_input("Depth Y [mm]", 0.0, 500.0, 0.0, 5.0)
    neck_height = st.number_input("Neck [mm]", 0.0, 200.0, 20.0, 5.0)
    mould_top_z = st.number_input("Top Z [mm]", value=250.0, step=10.0)
    mould_center_x = st.number_input("Center X [mm]", value=0.0, step=10.0)
    mould_center_y = st.number_input("Center Y [mm]", value=0.0, step=10.0)
    st.subheader("🔫 Lance")
    lance_length = st.selectbox("Length [mm]", [200, 250, 300], 1)
    st.subheader("🤖 Robot")
    nozzle_offset = st.number_input("Nozzle offset [mm]", 0.0, value=0.0, step=1.0)
    spray_cone_angle = st.number_input("Cone angle [deg]", 1.0, 90.0, 30.0, 5.0)
    target_spray_dist = st.number_input("Spray dist [mm]", 1.0, value=50.0, step=5.0)
    min_clearance = st.number_input("Min clearance [mm]", 1.0, value=10.0, step=1.0)
    nominal_speed = st.number_input("Nominal speed [mm/s]", 10.0, value=200.0, step=10.0)
    min_speed = st.number_input("Min speed [mm/s]", 1.0, value=50.0, step=10.0)
    max_speed = st.number_input("Max speed [mm/s]", 10.0, value=500.0, step=10.0)
    valve_delay = st.number_input("Valve delay [ms]", 0.0, value=50.0, step=10.0)
    coating_target = st.number_input("Coating target", 0.01, 1.0, 1.0, 0.05)
    st.subheader("🔄 Swabbing (3D)")
    swab_step = st.number_input("Swab step [mm]", 1.0, value=10.0, step=1.0)
    include_swab_up = st.checkbox("Include swab-up", False)
    approach_height = st.number_input("Approach height [mm]", 10.0, value=50.0, step=10.0)
    entry_offset_x = st.number_input("X offset [mm]", value=0.0, step=5.0)
    swab_center_y = st.number_input("Swab center Y [mm]", value=0.0, step=5.0)
    include_y_sweep = st.checkbox("Include Y sweep", False)
    swab_y_range = st.number_input("Y sweep range [mm]", 0.0, value=50.0, step=5.0) if include_y_sweep else 0.0
    swab_y_step = st.number_input("Y step [mm]", 1.0, value=10.0, step=1.0) if include_y_sweep else 10.0
    
    st.markdown("**Wait position offsets**")
    w1, w2, w3 = st.columns(3)
    with w1:
        wait_offset_x = st.number_input("Wait X offset [mm]", value=0.0, step=5.0, key="wox")
    with w2:
        wait_offset_y = st.number_input("Wait Y offset [mm]", value=0.0, step=5.0, key="woy")
    with w3:
        wait_offset_z = st.number_input("Wait Z offset [mm]", value=0.0, step=5.0, key="woz")
    
    calc_btn = st.button("🚀 Calculate", type="primary", use_container_width=True)

if "obstacles" not in st.session_state:
    st.session_state.obstacles = [
        ObstacleEnvelope(
            name="deflector",
            obstacle_type=ObstacleType.DEFLECTOR,
            x_min_mm=-50.0, x_max_mm=50.0,
            y_min_mm=-50.0, y_max_mm=50.0,
            z_min_mm=500.0, z_max_mm=600.0,
            clearance_mm=5.0,
        ),
        # DEFLECTOR type obstacles are ignored for wait/approach Z calculation
        # (robot passes UNDER them). Other types condition the wait Z.
        ObstacleEnvelope(
            name="mold left",
            obstacle_type=ObstacleType.MOULD_UPPER_EDGE,
            x_min_mm=-50.0, x_max_mm=-20.0,
            y_min_mm=-60.0, y_max_mm=60.0,
            z_min_mm=100.0, z_max_mm=250.0,
            clearance_mm=10.0,
        ),
        ObstacleEnvelope(
            name="mold right",
            obstacle_type=ObstacleType.MOULD_UPPER_EDGE,
            x_min_mm=20.0, x_max_mm=50.0,
            y_min_mm=-60.0, y_max_mm=60.0,
            z_min_mm=100.0, z_max_mm=250.0,
            clearance_mm=10.0,
        ),
    ]
if "trajectory_result" not in st.session_state: st.session_state.trajectory_result = None
if "config" not in st.session_state: st.session_state.config = None

st.subheader("🚧 Obstacles (3D)")
st.caption("Each obstacle has Edit (✏️) and Remove (🗑️) actions. DEFLECTOR types are excluded from wait Z calc (robot passes under).")
c1, c2, c3 = st.columns(3)
with c1:
    obs_name = st.text_input("Name", key="on")
    obs_type = st.selectbox("Type", [t.value for t in ObstacleType], key="ot")
    obs_x_min = st.number_input("X min", value=-50.0, step=5.0, key="ox1")
    obs_y_min = st.number_input("Y min", value=-50.0, step=5.0, key="oy1")
with c2:
    obs_clearance = st.number_input("Clearance [mm]", 0.0, value=5.0, step=1.0, key="oc")
    obs_x_max = st.number_input("X max", value=50.0, step=5.0, key="ox2")
    obs_y_max = st.number_input("Y max", value=50.0, step=5.0, key="oy2")
with c3:
    st.write("")
    obs_z_min = st.number_input("Z min", value=200.0, step=5.0, key="oz1")
    obs_z_max = st.number_input("Z max", value=230.0, step=5.0, key="oz2")
    add_obs = st.button("➕ Add", use_container_width=True)

if add_obs and obs_name.strip():
    try:
        st.session_state.obstacles.append(ObstacleEnvelope(obs_name.strip(), ObstacleType(obs_type), obs_x_min, obs_x_max, obs_y_min, obs_y_max, obs_z_min, obs_z_max, obs_clearance))
        st.success("Added!")
    except ValueError as e: st.error(str(e))

st.subheader("📦 Import from STL")
stl_file = st.file_uploader("Upload STL file", type=["stl"])
if stl_file is not None:
    # Save the uploaded file to a temporary location
    upload_dir = os.path.join("data", "uploaded_stl")
    os.makedirs(upload_dir, exist_ok=True)
    stl_path = os.path.join(upload_dir, stl_file.name)
    with open(stl_path, "wb") as f:
        f.write(stl_file.getbuffer())
    # Input parameters for the obstacle
    stl_name = st.text_input("Obstacle name", value=os.path.splitext(stl_file.name)[0])
    stl_type = st.selectbox("Obstacle type", [t.value for t in ObstacleType], key="stl_type")
    stl_clearance = st.number_input("Clearance [mm]", 0.0, value=5.0, step=1.0, key="stl_clearance")
    stl_col1, stl_col2, stl_col3 = st.columns(3)
    with stl_col1:
        stl_ref_x = st.number_input("Reference X [mm]", value=0.0, step=5.0, key="stl_ref_x")
    with stl_col2:
        stl_ref_y = st.number_input("Reference Y [mm]", value=0.0, step=5.0, key="stl_ref_y")
    with stl_col3:
        stl_ref_z = st.number_input("Reference Z [mm]", value=0.0, step=5.0, key="stl_ref_z")
    if st.button("Load STL as Obstacle", key="load_stl"):
        try:
            obstacle = ObstacleEnvelope.from_stl(
                filepath=stl_path,
                name=stl_name.strip(),
                obstacle_type=ObstacleType(stl_type),
                clearance_mm=stl_clearance,
                reference_point=(stl_ref_x, stl_ref_y, stl_ref_z)
            )
            st.session_state.obstacles.append(obstacle)
            st.success("STL loaded as obstacle!")
        except Exception as e:
            st.error(f"Failed to load STL: {e}")
if st.button("🗑️ Clear all"): st.session_state.obstacles = []
if st.session_state.obstacles:
    for i, obs in enumerate(st.session_state.obstacles):
        with st.expander(f"{obs.name}"):
            st.write(f"X:[{obs.x_min_mm:.1f},{obs.x_max_mm:.1f}] Y:[{obs.y_min_mm:.1f},{obs.y_max_mm:.1f}] Z:[{obs.z_min_mm:.1f},{obs.z_max_mm:.1f}]")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"✏️ Edit {i}", key=f"edit_{i}"):
                    st.session_state.editing_obs_idx = i
                    st.session_state.edit_name = obs.name
                    st.session_state.edit_type = obs.obstacle_type.value
                    st.session_state.edit_x_min = obs.x_min_mm
                    st.session_state.edit_x_max = obs.x_max_mm
                    st.session_state.edit_y_min = obs.y_min_mm
                    st.session_state.edit_y_max = obs.y_max_mm
                    st.session_state.edit_z_min = obs.z_min_mm
                    st.session_state.edit_z_max = obs.z_max_mm
                    st.session_state.edit_clearance = obs.clearance_mm
                    st.rerun()
            with c2:
                if st.button(f"🗑️ Remove {i}", key=f"remove_{i}"):
                    st.session_state.obstacles.pop(i)
                    st.rerun()

# Edit obstacle form
if "editing_obs_idx" in st.session_state and st.session_state.editing_obs_idx is not None:
    idx = st.session_state.editing_obs_idx
    if idx < len(st.session_state.obstacles):
        obs = st.session_state.obstacles[idx]
        with st.form(f"edit_form_{idx}"):
            st.subheader(f"Editing: {obs.name}")
            e1, e2, e3 = st.columns(3)
            with e1:
                edit_name = st.text_input("Name", value=st.session_state.get("edit_name", obs.name), key=f"en_{idx}")
                edit_type = st.selectbox("Type", [t.value for t in ObstacleType], index=[t.value for t in ObstacleType].index(st.session_state.get("edit_type", obs.obstacle_type.value)), key=f"et_{idx}")
                edit_x_min = st.number_input("X min", value=st.session_state.get("edit_x_min", obs.x_min_mm), step=5.0, key=f"ex1_{idx}")
                edit_y_min = st.number_input("Y min", value=st.session_state.get("edit_y_min", obs.y_min_mm), step=5.0, key=f"ey1_{idx}")
            with e2:
                edit_clearance = st.number_input("Clearance [mm]", 0.0, value=st.session_state.get("edit_clearance", obs.clearance_mm), step=1.0, key=f"ec_{idx}")
                edit_x_max = st.number_input("X max", value=st.session_state.get("edit_x_max", obs.x_max_mm), step=5.0, key=f"ex2_{idx}")
                edit_y_max = st.number_input("Y max", value=st.session_state.get("edit_y_max", obs.y_max_mm), step=5.0, key=f"ey2_{idx}")
            with e3:
                st.write("")
                edit_z_min = st.number_input("Z min", value=st.session_state.get("edit_z_min", obs.z_min_mm), step=5.0, key=f"ez1_{idx}")
                edit_z_max = st.number_input("Z max", value=st.session_state.get("edit_z_max", obs.z_max_mm), step=5.0, key=f"ez2_{idx}")
            save_edit, cancel_edit = st.columns(2)
            with save_edit:
                if st.form_submit_button("💾 Save", use_container_width=True):
                    try:
                        new_name = edit_name.strip() if edit_name else obs.name
                        st.session_state.obstacles[idx] = ObstacleEnvelope(
                            new_name, ObstacleType(edit_type),
                            edit_x_min, edit_x_max, edit_y_min, edit_y_max,
                            edit_z_min, edit_z_max, edit_clearance
                        )
                        del st.session_state.editing_obs_idx
                        st.success("Saved!")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
            with cancel_edit:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    del st.session_state.editing_obs_idx
                    st.rerun()

if calc_btn:
    with st.spinner("Calculating..."):
        try:
            mould = MouldGeometry(mould_diameter, mould_height, neck_height, mould_top_z, mould_center_x, mould_center_y, mould_depth)
            robot = RobotParameters(lance_length, nozzle_offset, spray_cone_angle, target_spray_dist, min_clearance, max_speed, min_speed, nominal_speed, valve_delay, coating_target)
            swab = SwabbingParameters(
                reference_diameter_mm=mould_diameter,
                coating_start_z_mm=mould_top_z,
                coating_end_z_mm=mould.mould_bottom_z_mm,
                swab_step_mm=swab_step,
                include_swab_up=include_swab_up,
                entry_offset_x_mm=entry_offset_x,
                approach_height_mm=approach_height,
                swab_center_y_mm=swab_center_y,
                include_y_sweep=include_y_sweep,
                swab_y_range_mm=swab_y_range,
                swab_y_step_mm=swab_y_step,
                wait_offset_x_mm=wait_offset_x,
                wait_offset_y_mm=wait_offset_y,
                wait_offset_z_mm=wait_offset_z,
            )
            result = generate_trajectory(mould, st.session_state.obstacles, robot, swab)
            config = ProjectConfiguration("Session3D", mould, list(st.session_state.obstacles), robot, swab)
            st.session_state.trajectory_result = result
            st.session_state.config = config
        except ValueError as e: st.error(f"Error: {e}")

if st.session_state.trajectory_result:
    res = st.session_state.trajectory_result
    cfg = st.session_state.config
    st.subheader("📊 Results")
    if res.feasible: st.success("✅ FEASIBLE")
    else: st.error("❌ COLLISIONS")
    m1, m2, m3 = st.columns(3)
    m1.metric("Points", res.total_points)
    m2.metric("Min Clearance", f"{res.min_clearance_margin_mm:.1f} mm" if res.min_clearance_margin_mm != float("inf") else "∞")
    m3.metric("Warnings", len([p for p in res.points if p.collision_status.name == "WARNING"]))
    
    st.subheader("🎯 3D View")
    use_interactive_3d = st.checkbox("Interactive 3D (pan/tilt/zoom)", value=True, key="interactive_3d")
    try:
        if use_interactive_3d:
            fig3d = create_trajectory_plot_3d_interactive(cfg.mould, cfg.obstacles, res, cfg.robot_params.minimum_clearance_mm)
            st.plotly_chart(fig3d, use_container_width=True)
        else:
            fig3d = create_trajectory_plot_3d(cfg.mould, cfg.obstacles, res, cfg.robot_params.minimum_clearance_mm)
            st.pyplot(fig3d)
    except ImportError as e:
        st.warning(f"Interactive 3D not available: {e}. Falling back to static plot.")
        fig3d = create_trajectory_plot_3d(cfg.mould, cfg.obstacles, res, cfg.robot_params.minimum_clearance_mm)
        st.pyplot(fig3d)
    
    st.subheader("📐 Projections")
    fig2d = create_projection_plots(cfg.mould, cfg.obstacles, res, cfg.robot_params.minimum_clearance_mm)
    st.pyplot(fig2d)
    
    with st.expander("📋 Trajectory points", True):
        import pandas as pd
        df = pd.DataFrame([{"ID":p.point_id,"X":p.x_mm,"Y":p.y_mm,"Z":p.z_mm,"Speed":p.speed_mm_s,"Valve":p.valve_state.value,"Segment":p.segment_type.value,"Status":p.collision_status.value} for p in res.points])
        st.dataframe(df, use_container_width=True)
    
    st.subheader("💾 Export")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("CSV"):
            p = export_csv(res, "outputs/traj.csv")
            st.download_button("Download CSV", open(p).read(), "trajectory.csv", "text/csv")
    with c2:
        if st.button("JSON"):
            p = export_json(cfg, res, "outputs/traj.json")
            st.download_button("Download JSON", open(p).read(), "trajectory.json", "application/json")
    with c3:
        if st.button("Report"):
            p = generate_report(cfg, res, "outputs/report.md")
            st.download_button("Download Report", open(p).read(), "report.md", "text/markdown")

def _sample_obs():
    return [
        ObstacleEnvelope("Deflector", ObstacleType.DEFLECTOR, -100, 100, -50, 50, 210, 240, 8),
        ObstacleEnvelope("Baffle", ObstacleType.BAFFLE_MECHANISM, -120, -40, -60, 0, 160, 260, 5),
        ObstacleEnvelope("Funnel", ObstacleType.FUNNEL_MECHANISM, 40, 120, 0, 60, 160, 260, 5),
    ]