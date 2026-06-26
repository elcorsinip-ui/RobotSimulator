"""
RobotSimulator — Version Module

Centralized version management for the project.
Version string is read from VERSION file in the project root.
"""

from __future__ import annotations

import os
import datetime

# ============================================================================
# Version reading
# ============================================================================

_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_PACKAGE_DIR, ".."))
_VERSION_FILE = os.path.join(_PROJECT_ROOT, "VERSION")


def _read_version() -> str:
    """Read version from VERSION file. Fallback to '0.0.0+dev' if missing."""
    try:
        with open(_VERSION_FILE, "r") as f:
            return f.read().strip()
    except (FileNotFoundError, IOError):
        return "0.0.0+dev"


# ============================================================================
# Public constants
# ============================================================================

VERSION = _read_version()
"""Semantic version string (e.g. '0.2.0'). Read from VERSION file."""

BUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
"""Build/run date in ISO format."""

VERSION_STRING = f"{VERSION} (build {BUILD_DATE})"
"""Full human-readable version string."""

PROJECT_NAME = "RobotSimulator"
"""Project display name."""

PROJECT_DESCRIPTION = (
    "FANUC Robot Swabbing Trajectory Calculator "
    "for IS Hollow Glass Forming Machine — Blank Side"
)
"""One-line project description."""

GITHUB_URL = "https://github.com/BotteroGroup/RobotSimulator"
"""Placeholder GitHub repository URL. Update before publishing."""

LICENSE = "Proprietary — Bottero Group S.p.A."
"""License identifier. Update before publishing."""

COPYRIGHT_YEAR = "2026"
"""Copyright year."""

COPYRIGHT_HOLDER = "Bottero Group S.p.A."
"""Copyright holder."""


# ============================================================================
# Disclaimer
# ============================================================================

ENGINEERING_DISCLAIMER = f"""
# ⚠️ ENGINEERING TOOL ONLY — NOT A CERTIFIED SAFETY SYSTEM

**{PROJECT_NAME} v{VERSION}**

This software is an engineering support tool for the configuration and calculation
of FANUC robot swabbing trajectories. It is NOT a certified safety system.

## Mandatory Warnings

1. **Final trajectory MUST be validated** by robot offline simulation (e.g. FANUC ROBOGUIDE)
   or real dry-run at low speed before any production use.

2. **Final robot path MUST be validated** against the real FANUC robot reachability,
   joint limits, and axis configuration.

3. **The system does NOT replace** machine risk assessment as required by
   ISO 12100 / ISO 10218 / relevant local regulations.

4. **Collision checks are valid ONLY** for the geometry entered by the user.
   Any deviation between entered geometry and the real machine voids collision guarantees.

5. **Safety clearances MUST be reviewed** by a qualified mechanical, automation or
   process engineer familiar with the specific IS machine configuration.

6. **Any real implementation on an IS machine MUST be validated** with:
   - Lockout/tagout (LOTO) per machine safety procedures
   - Dry-run at reduced speed (max 10% of nominal)
   - Full customer safety procedure and site-specific risk assessment
   - Presence of qualified personnel during first operation

## Liability

The authors, contributors, and distributors of this software assume no liability for
any damage, injury, or loss resulting from the use of this tool. Use at your own risk.

**{COPYRIGHT_HOLDER} © {COPYRIGHT_YEAR}. All rights reserved.**
""".strip()


# ============================================================================
# Quick access
# ============================================================================

def print_info() -> None:
    """Print version and project info to stdout."""
    print(f"{PROJECT_NAME} v{VERSION}")
    print(f"Build: {BUILD_DATE}")
    print(f"License: {LICENSE}")
    print(f"Copyright © {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}")
    print()
    print("Disclaimer:")
    print(ENGINEERING_DISCLAIMER[:200] + "...")


if __name__ == "__main__":
    print_info()