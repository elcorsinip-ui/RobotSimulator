# RobotSimulator — User Guide

## Installation

```bash
cd /root/RobotSimulator
pip install -r requirements.txt
```

## Run Streamlit Web App

```bash
streamlit run app.py
```

Open browser at: http://localhost:8501

## Input Parameters

### Sidebar — Mould Geometry
- Mould diameter [mm]: inner diameter of blank mould
- Mould height [mm]: cavity height
- Neck height [mm]: neck ring below mould
- Mould top Z [mm]: upper edge Z coordinate
- Mould center X [mm]: centerline X coordinate

### Sidebar — Lance Selection
- 200, 250, or 300 mm

### Sidebar — Robot Parameters
- Nozzle offset [mm]
- Spray cone angle [deg]
- Target spray distance [mm]
- Minimum clearance [mm]
- Nominal / min / max speed [mm/s]
- Valve delay [ms]
- Coating target (relative)

### Sidebar — Swabbing Process
- Swab step [mm]
- Include swab-up pass
- Approach height above obstacles [mm]
- Entry X offset [mm]

### Main Area — Obstacles (3D)
Add obstacles by name, type, X/Y/Z boundaries, clearance. 

**Default obstacle:** A "deflector" obstacle is pre-loaded (type: DEFLECTOR, Z: 500-600mm, X: -50 to 50mm, Y: -50 to 50mm). Deflectors represent upper obstacles the robot passes UNDER — they do NOT condition the wait/approach Z height.

**Actions per obstacle:**
- ✏️ **Edit** — modify name, type, coordinates, clearance
- 🗑️ **Remove** — delete obstacle from list
- 🗑️ **Clear all** — remove all obstacles

**Obstacle types:**
- `DEFLECTOR` — upper obstacle, robot passes under (excluded from wait Z calc)
- `MOULD_UPPER_EDGE` — mould top edge (conditions wait Z)
- `BAFFLE_MECHANISM`, `FUNNEL_MECHANISM`, `MACHINE_FRAME`, `CUSTOM` — condition wait Z

## Output

- X-Z plot visualization
- Trajectory table
- Feasibility indicator
- CSV / JSON / Markdown export buttons


## STL Obstacle Import

You can import obstacles from STL files via the sidebar:

1. Click "📤 Import from STL" in the sidebar.
2. Upload an STL file (binary or ASCII).
3. Set the obstacle name, type, clearance, and reference point (the point where the minimum corner of the STL's bounding box will be placed).
4. Press "Load STL as Obstacle".

The STL's bounding box is used for collision calculations and for determining the obstacle's influence on wait/approach heights. The actual mesh is rendered in the 3D view (if interactive 3D is enabled) for better visualization.

Note: The obstacle's collision shape remains an axis-aligned bounding box (this will be refined in a future update).

## Safety Warnings

Trajectory must be validated by real dry-run at low speed before use on production.
