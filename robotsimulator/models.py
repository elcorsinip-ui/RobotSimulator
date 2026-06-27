"""
RobotSimulator — Data Models (3D)

All dataclasses for the FANUC robot swabbing trajectory calculator.
Includes validation, obstacle types, segment types, and trajectory structures.

Coordinate System (3D):
    X: horizontal, 0 at mould centerline, positive toward robot side (blank side)
    Y: depth, 0 at machine datum, positive along the mould axis
    Z: vertical, 0 at machine datum, positive upward
    All dimensions in millimeters
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ============================================================================
# Enumerations
# ============================================================================

class ObstacleType(str, Enum):
    """Types of obstacles on the blank side of an IS machine."""
    MOULD_UPPER_EDGE = "mould_upper_edge"
    DEFLECTOR = "deflector"
    BAFFLE_MECHANISM = "baffle_mechanism"
    FUNNEL_MECHANISM = "funnel_mechanism"
    MACHINE_FRAME = "machine_frame"
    CUSTOM = "custom"


class SegmentType(str, Enum):
    """Trajectory segment types."""
    WAIT = "wait"
    APPROACH = "approach"
    ENTER = "enter"
    SWAB_DOWN = "swab_down"
    SWAB_UP = "swab_up"
    EXIT = "exit"


class CollisionStatus(str, Enum):
    """Collision check result for a trajectory point."""
    CLEAR = "clear"
    WARNING = "warning"
    COLLISION = "collision"


class ValveState(str, Enum):
    """Valve state at a trajectory point."""
    OFF = "OFF"
    ON = "ON"


# ============================================================================
# Mould Geometry (3D)
# ============================================================================

@dataclass
class MouldGeometry:
    """
    Geometry of the blank mould on an IS machine (3D).

    The mould is modeled as a vertical cylinder in 3D space.
    Z=0 is at machine datum; mould_top_z_mm is the Z coordinate
    of the upper wire / top edge of the mould.

    The mould now has a Y dimension to represent the depth/length
    of the mould cavity along the Y axis.

    Derived properties:
        mould_bottom_z_mm: Z coordinate of the mould cavity bottom
        neck_bottom_z_mm: Z coordinate of the neck ring bottom
        mould_left_x_mm: left edge of the mould (X - radius)
        mould_right_x_mm: right edge of the mould (X + radius)
        mould_front_y_mm: front edge of the mould (Y - depth/2)
        mould_back_y_mm: back edge of the mould (Y + depth/2)
        mould_radius_mm: mould radius
    """
    mould_diameter_mm: float
    mould_height_mm: float
    neck_height_mm: float = 0.0
    mould_top_z_mm: float = 0.0
    mould_center_x_mm: float = 0.0
    mould_center_y_mm: float = 0.0
    mould_depth_mm: float = 0.0  # NEW: Y dimension (0 = circular, use diameter)

    def __post_init__(self):
        if self.mould_diameter_mm <= 0:
            raise ValueError(f"mould_diameter_mm must be > 0, got {self.mould_diameter_mm}")
        if self.mould_height_mm <= 0:
            raise ValueError(f"mould_height_mm must be > 0, got {self.mould_height_mm}")
        if self.neck_height_mm < 0:
            raise ValueError(f"neck_height_mm must be >= 0, got {self.neck_height_mm}")
        if self.mould_depth_mm < 0:
            raise ValueError(f"mould_depth_mm must be >= 0, got {self.mould_depth_mm}")

    @property
    def mould_bottom_z_mm(self) -> float:
        return self.mould_top_z_mm - self.mould_height_mm

    @property
    def neck_bottom_z_mm(self) -> float:
        return self.mould_bottom_z_mm - self.neck_height_mm

    @property
    def mould_left_x_mm(self) -> float:
        return self.mould_center_x_mm - self.mould_diameter_mm / 2.0

    @property
    def mould_right_x_mm(self) -> float:
        return self.mould_center_x_mm + self.mould_diameter_mm / 2.0

    @property
    def mould_radius_mm(self) -> float:
        return self.mould_diameter_mm / 2.0

    @property
    def mould_front_y_mm(self) -> float:
        """Front edge of mould in Y (negative direction from center)."""
        if self.mould_depth_mm > 0:
            return self.mould_center_y_mm - self.mould_depth_mm / 2.0
        return self.mould_center_y_mm - self.mould_diameter_mm / 2.0

    @property
    def mould_back_y_mm(self) -> float:
        """Back edge of mould in Y (positive direction from center)."""
        if self.mould_depth_mm > 0:
            return self.mould_center_y_mm + self.mould_depth_mm / 2.0
        return self.mould_center_y_mm + self.mould_diameter_mm / 2.0

    @property
    def effective_y_depth_mm(self) -> float:
        """Effective Y depth (use mould_depth_mm if set, otherwise diameter)."""
        return self.mould_depth_mm if self.mould_depth_mm > 0 else self.mould_diameter_mm


# ============================================================================
# Obstacle Envelope (3D Box)
# ============================================================================

@dataclass
class ObstacleEnvelope:
    """
    Rectangular obstacle envelope in 3D (X-Y-Z box).

    Each obstacle is defined by its 3D bounding box and a local
    safety clearance that expands the forbidden zone in all directions.
    """
    name: str
    obstacle_type: ObstacleType
    x_min_mm: float
    x_max_mm: float
    y_min_mm: float
    y_max_mm: float
    z_min_mm: float
    z_max_mm: float
    clearance_mm: float = 0.0

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Obstacle name must not be empty")
        # Convert string obstacle_type to enum if needed
        if isinstance(self.obstacle_type, str):
            try:
                self.obstacle_type = ObstacleType(self.obstacle_type)
            except ValueError:
                valid = ", ".join(t.value for t in ObstacleType)
                raise ValueError(
                    f"Invalid obstacle_type '{self.obstacle_type}'. "
                    f"Valid values: {valid}"
                )
        if self.x_min_mm >= self.x_max_mm:
            raise ValueError(
                f"x_min_mm ({self.x_min_mm}) must be < x_max_mm ({self.x_max_mm})"
            )
        if self.y_min_mm >= self.y_max_mm:
            raise ValueError(
                f"y_min_mm ({self.y_min_mm}) must be < y_max_mm ({self.y_max_mm})"
            )
        if self.z_min_mm >= self.z_max_mm:
            raise ValueError(
                f"z_min_mm ({self.z_min_mm}) must be < z_max_mm ({self.z_max_mm})"
            )
        if self.clearance_mm < 0:
            raise ValueError(f"clearance_mm must be >= 0, got {self.clearance_mm}")

    @property
    def expanded_x_min_mm(self) -> float:
        """Left boundary including clearance."""
        return self.x_min_mm - self.clearance_mm

    @property
    def expanded_x_max_mm(self) -> float:
        """Right boundary including clearance."""
        return self.x_max_mm + self.clearance_mm

    @property
    def expanded_y_min_mm(self) -> float:
        """Front boundary including clearance."""
        return self.y_min_mm - self.clearance_mm

    @property
    def expanded_y_max_mm(self) -> float:
        """Back boundary including clearance."""
        return self.y_max_mm + self.clearance_mm

    @property
    def expanded_z_min_mm(self) -> float:
        """Bottom boundary including clearance."""
        return self.z_min_mm - self.clearance_mm

    @property
    def expanded_z_max_mm(self) -> float:
        """Top boundary including clearance."""
        return self.z_max_mm + self.clearance_mm

    @property
    def center_x_mm(self) -> float:
        return (self.x_min_mm + self.x_max_mm) / 2.0

    @property
    def center_y_mm(self) -> float:
        return (self.y_min_mm + self.y_max_mm) / 2.0

    @property
    def center_z_mm(self) -> float:
        return (self.z_min_mm + self.z_max_mm) / 2.0

    @property
    def width_mm(self) -> float:
        return self.x_max_mm - self.x_min_mm

    @property
    def depth_mm(self) -> float:
        return self.y_max_mm - self.y_min_mm

    @property
    def height_mm(self) -> float:
        return self.z_max_mm - self.z_min_mm

    @property
    def volume_mm3(self) -> float:
        """Volume of the obstacle in cubic millimeters."""
        return self.width_mm * self.depth_mm * self.height_mm


# ============================================================================
# Robot Parameters
# ============================================================================

VALID_LANCE_LENGTHS = {200, 250, 300}


@dataclass
class RobotParameters:
    """
    Robot and swabbing lance parameters.

    The lance is assumed vertical (first-order model).
    The nozzle offset is the distance from the lance tip to the spray point.
    """
    lance_length_mm: int
    nozzle_offset_mm: float = 0.0
    spray_cone_angle_deg: float = 30.0
    target_spray_distance_mm: float = 50.0
    minimum_clearance_mm: float = 10.0
    max_robot_speed_mm_s: float = 500.0
    min_robot_speed_mm_s: float = 50.0
    nominal_speed_mm_s: float = 200.0
    valve_delay_ms: float = 50.0
    coating_target_relative: float = 1.0

    def __post_init__(self):
        if self.lance_length_mm not in VALID_LANCE_LENGTHS:
            raise ValueError(
                f"lance_length_mm must be one of {VALID_LANCE_LENGTHS}, "
                f"got {self.lance_length_mm}"
            )
        if self.nozzle_offset_mm < 0:
            raise ValueError(
                f"nozzle_offset_mm must be >= 0, got {self.nozzle_offset_mm}"
            )
        if not (0 < self.spray_cone_angle_deg <= 90):
            raise ValueError(
                f"spray_cone_angle_deg must be in (0, 90], "
                f"got {self.spray_cone_angle_deg}"
            )
        if self.target_spray_distance_mm <= 0:
            raise ValueError(
                f"target_spray_distance_mm must be > 0, "
                f"got {self.target_spray_distance_mm}"
            )
        if self.minimum_clearance_mm <= 0:
            raise ValueError(
                f"minimum_clearance_mm must be > 0, "
                f"got {self.minimum_clearance_mm}"
            )
        if self.min_robot_speed_mm_s <= 0:
            raise ValueError(
                f"min_robot_speed_mm_s must be > 0, "
                f"got {self.min_robot_speed_mm_s}"
            )
        if self.max_robot_speed_mm_s <= self.min_robot_speed_mm_s:
            raise ValueError(
                f"max_robot_speed_mm_s ({self.max_robot_speed_mm_s}) must be > "
                f"min_robot_speed_mm_s ({self.min_robot_speed_mm_s})"
            )
        if not (self.min_robot_speed_mm_s <= self.nominal_speed_mm_s <= self.max_robot_speed_mm_s):
            raise ValueError(
                f"nominal_speed_mm_s ({self.nominal_speed_mm_s}) must be between "
                f"min ({self.min_robot_speed_mm_s}) and max ({self.max_robot_speed_mm_s})"
            )
        if self.valve_delay_ms < 0:
            raise ValueError(
                f"valve_delay_ms must be >= 0, got {self.valve_delay_ms}"
            )
        if not (0 < self.coating_target_relative <= 1.0):
            raise ValueError(
                f"coating_target_relative must be in (0, 1], "
                f"got {self.coating_target_relative}"
            )


# ============================================================================
# Swabbing Parameters (3D)
# ============================================================================

@dataclass
class SwabbingParameters:
    """
    Parameters controlling the swabbing path generation (3D).

    These are derived or user-specified values that guide
    how the trajectory is built inside the mould.

    NEW for 3D:
        - swab_y_positions: list of Y positions to swab (multiple passes)
        - swab_y_step_mm: step in Y between multiple swab passes
        - include_y_sweep: whether to sweep in Y direction during swabbing
    """
    reference_diameter_mm: float = 0.0  # Default: set to mould_diameter_mm
    coating_start_z_mm: float = 0.0     # Set to mould_top_z_mm
    coating_end_z_mm: float = 0.0       # Set to mould_bottom_z_mm
    swab_step_mm: float = 10.0          # Vertical step between swab points
    include_swab_up: bool = False        # Whether to include an upward swab pass
    entry_offset_x_mm: float = 0.0     # X offset from centre if direct path blocked
    approach_height_mm: float = 50.0   # Height above highest obstacle for approach
    
    # NEW 3D parameters
    swab_center_y_mm: float = 0.0      # Y center for swabbing
    include_y_sweep: bool = False       # Whether to sweep in Y direction
    swab_y_range_mm: float = 0.0       # Total Y range to sweep
    swab_y_step_mm: float = 10.0       # Y step between sweep passes

    # Wait position offsets (relative to mould center + diameter)
    wait_offset_x_mm: float = 0.0       # X offset from mould center + radius + 10mm default
    wait_offset_y_mm: float = 0.0       # Y offset from mould center
    wait_offset_z_mm: float = 0.0       # Z offset from approach height

    def __post_init__(self):
        if self.reference_diameter_mm < 0:
            raise ValueError(
                f"reference_diameter_mm must be >= 0, "
                f"got {self.reference_diameter_mm}"
            )
        if self.swab_step_mm <= 0:
            raise ValueError(
                f"swab_step_mm must be > 0, got {self.swab_step_mm}"
            )
        if self.approach_height_mm <= 0:
            raise ValueError(
                f"approach_height_mm must be > 0, "
                f"got {self.approach_height_mm}"
            )
        if self.swab_y_range_mm < 0:
            raise ValueError(
                f"swab_y_range_mm must be >= 0, got {self.swab_y_range_mm}"
            )
        if self.swab_y_step_mm <= 0:
            raise ValueError(
                f"swab_y_step_mm must be > 0, got {self.swab_y_step_mm}"
            )


# ============================================================================
# Trajectory Point (3D)
# ============================================================================

@dataclass
class TrajectoryPoint:
    """
    A single point on the robot swabbing trajectory (3D).

    Each point carries its 3D coordinates, speed, valve state,
    segment classification, and collision status.
    """
    point_id: int
    x_mm: float
    y_mm: float  # NEW: Y coordinate
    z_mm: float
    speed_mm_s: float
    valve_state: ValveState = ValveState.OFF
    segment_type: SegmentType = SegmentType.WAIT
    collision_status: CollisionStatus = CollisionStatus.CLEAR
    clearance_margin_mm: float = float("inf")
    note: str = ""

    def __post_init__(self):
        if self.point_id < 0:
            raise ValueError(f"point_id must be >= 0, got {self.point_id}")
        if self.speed_mm_s < 0:
            raise ValueError(f"speed_mm_s must be >= 0, got {self.speed_mm_s}")
    
    @property
    def position_3d(self) -> tuple:
        """Return (x, y, z) tuple."""
        return (self.x_mm, self.y_mm, self.z_mm)


# ============================================================================
# Trajectory Result
# ============================================================================

@dataclass
class TrajectoryResult:
    """
    Complete trajectory result including all points,
    collision warnings, and feasibility status.
    """
    points: List[TrajectoryPoint] = field(default_factory=list)
    collision_warnings: List[str] = field(default_factory=list)
    feasible: bool = True

    @property
    def total_points(self) -> int:
        return len(self.points)

    @property
    def has_collisions(self) -> bool:
        return any(
            p.collision_status == CollisionStatus.COLLISION
            for p in self.points
        )

    @property
    def has_warnings(self) -> bool:
        return any(
            p.collision_status == CollisionStatus.WARNING
            for p in self.points
        )

    @property
    def min_clearance_margin_mm(self) -> float:
        """Minimum clearance margin across all trajectory points."""
        if not self.points:
            return float("inf")
        return min(p.clearance_margin_mm for p in self.points)


# ============================================================================
# Project Configuration (complete input set)
# ============================================================================

@dataclass
class ProjectConfiguration:
    """
    Complete project configuration bundling all inputs
    needed for trajectory generation.
    """
    project_name: str = "RobotSwabbing_Project"
    mould: MouldGeometry = None
    obstacles: List[ObstacleEnvelope] = field(default_factory=list)
    robot_params: RobotParameters = None
    swabbing_params: SwabbingParameters = None

    def __post_init__(self):
        if self.mould is None:
            self.mould = MouldGeometry(
                mould_diameter_mm=150.0,
                mould_height_mm=120.0,
                neck_height_mm=20.0,
            )
        if self.robot_params is None:
            self.robot_params = RobotParameters(lance_length_mm=250)
        if self.swabbing_params is None:
            self.swabbing_params = SwabbingParameters()