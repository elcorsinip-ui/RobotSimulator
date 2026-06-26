"""
RobotSimulator — FANUC Robot Swabbing Trajectory Calculator
for IS Hollow Glass Forming Machine — Blank Side

Engineering application for configuring and calculating
ideal X-Z swabbing trajectories.
"""

from __future__ import annotations

from .version import (
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
    print_info as _print_info,
)

__version__ = VERSION
__build__ = BUILD_DATE
__description__ = PROJECT_DESCRIPTION
__github__ = GITHUB_URL
__license__ = LICENSE
__copyright__ = f"© {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}"