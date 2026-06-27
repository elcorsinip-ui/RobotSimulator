# Changelog

All notable changes to **RobotSimulator** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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