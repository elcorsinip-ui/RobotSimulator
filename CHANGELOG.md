# Changelog

All notable changes to **RobotSimulator** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2026-06-28

### Added
- **Obstacle type colors in 3D plots**: Each obstacle type now has distinct colors (DEFLECTOR=cyan, MOULD_UPPER_EDGE=brown, BAFFLE_MECHANISM=orange, FUNNEL_MECHANISM=purple, MACHINE_FRAME=grey, CUSTOM=red)
- **Semi-transparent face fills**: 3D obstacles show filled faces for better volume perception in both matplotlib and Plotly
- **Enhanced obstacle labels**: Labels now show both name and type (e.g., "deflector\n(DEFLECTOR)") with colored backgrounds

### Changed
- **Matplotlib 3D obstacles**: Type-based edge colors, face fills, and informative labels
- **Plotly Interactive 3D obstacles**: Type-based Mesh3d face fills, edge colors, and HTML labels with type info

## [0.3.2] - 2026-06-28

### Added
- **Obstacle edit/remove**: Each obstacle in the UI now has Edit (✏️) and Remove (🗑️) buttons
- **Default deflector obstacle**: Pre-loaded "deflector" obstacle (type DEFLECTOR, Z: 500-600mm, X/Y: -50 to 50mm) representing upper machine deflectors the robot passes under
- **DEFLECTOR exclusion logic**: Deflector-type obstacles are excluded from wait/approach Z height calculation (robot passes UNDER them)

### Changed
- **UI obstacle list**: Now shows expandable details with inline edit form
- **Obstacle management**: "Clear all" button plus per-obstacle remove

## [0.3.1] - 2026-06-27

### Added
- **Interactive 3D visualization**: Plotly-based 3D plot with native pan, tilt (rotate), and zoom in browser
- **Toggle in UI**: Checkbox "Interactive 3D (pan/tilt/zoom)" to switch between static (matplotlib) and interactive (Plotly) modes
- **Hover tooltips**: Point details on hover in interactive mode

### Changed
- **Requirements**: Added `plotly>=5.17.0` dependency

### Fixed
- Graceful fallback: If Plotly unavailable, automatically falls back to matplotlib static 3D plot

## [0.3.0] - 2026-06-27

### Added
- **3D visualization**: Complete 3D trajectory plots with mould, obstacles, and trajectory (matplotlib)
- **Wait position configuration**: User-configurable wait point offsets (X, Y, Z) in UI sidebar
- **Default mould obstacles**: Pre-loaded "mold left" and "mold right" obstacles (MOULD_UPPER_EDGE type)
- **Default parameter updates**: Mould diameter 60mm, height 250mm, top Z 250mm

### Fixed
- **3D plotting crashes**: Fixed `NameError: np not defined` (missing numpy import)
- **3D obstacle rendering**: Fixed `enumerate(expanded=True)` typo in `_draw_obstacles_3d`
- **Marker style errors**: Fixed `ValueError: Unrecognized marker style '!'` in both 3D and 2D plots (replaced with `*`)

### Changed
- **Wait point default**: Now at `mould_center_x + radius + 10mm` (was at swab_x)
- **Mould geometry**: Updated defaults for typical 60mm diameter blank mould

## [0.2.0] - 2026-06-26

### Added
- **Version management system**: `VERSION` file, `robotsimulator/version.py` module
- **Engineering disclaimer**: Full safety warning displayed in app expander at startup
- **Version display in UI**: Version, build date, license shown in header and sidebar
- **GitHub placeholder**: `GITHUB_URL` constant for future repository link
- **CHANGELOG.md**: This file for tracking releases
- **LICENSE** file placeholder (proprietary - Bottero Group)

### Changed
- Updated `robotsimulator/__init__.py` to export version constants
- Updated `app.py` to use centralized version module and show disclaimer
- Updated footer with dynamic version and GitHub link

### Fixed
- String-to-enum conversion in `ObstacleEnvelope` for JSON loading compatibility

## [0.1.0] - 2026-06-26

### Added
- Initial release with complete trajectory calculation engine
- Streamlit web interface
- Collision detection (rectangular obstacles)
- Velocity modulation (first-order model)
- Valve timing compensation
- Export system (CSV, JSON, Markdown report)
- X-Z trajectory visualization (matplotlib)
- Unit tests (59 tests passing)
- Documentation (architecture, user guide, engineering notes, validation plan)

---

## Future Releases (Planned)

### [0.3.0] - Planned
- Polygon obstacle support (non-rectangular)
- Variable mould diameter profile (tapered/conical moulds)
- Tilted lance orientation support
- FANUC TP/KAREL export (real robot code generation)

### [1.0.0] - Planned
- Production-ready release with full safety validation
- Multi-section IS machine support
- DXF/DWG import for machine geometry
- Integration with real robot controller (FANUC KAREL)
- Full risk assessment documentation