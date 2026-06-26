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

### Main Area — Obstacles
Add obstacles by name, type, X/Z boundaries, clearance. Click "Load sample obstacles"
for realistic defaults.

## Output

- X-Z plot visualization
- Trajectory table
- Feasibility indicator
- CSV / JSON / Markdown export buttons

## Safety Warnings

Trajectory must be validated by real dry-run at low speed before use on production.
