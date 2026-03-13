from dataclasses import dataclass
from typing import Tuple

from backend.config.environment import environment

@dataclass(frozen=True)
class SimulationConfig:
    """Centralized configuration for AegisSwarm simulation."""
    
    # Grid Settings
    GRID_SIZE: Tuple[int, int] = (20, 20)
    OBSTACLE_DENSITY: float = 0.15  # Percentage of grid with obstacles
    EVENT_DENSITY: float = 0.05     # Percentage of grid with environmental events
    
    # Robot Settings
    NUM_ROBOTS: int = 5
    INITIAL_ENERGY: float = 100.0
    SENSOR_RANGE: int = 3
    COVERAGE_MARK_RADIUS: int = 1
    MOVEMENT_SPEED: float = 1.0
    
    # Simulation Settings
    SIMULATION_SPEED: float = 0.2  # Seconds between steps
    MAX_STEPS: int = 100
    TARGET_COVERAGE_PERCENT: float = 95.0
    NO_PROGRESS_STEP_LIMIT: int = 20
    MISSION_TIMEOUT: int = 300     # Maximum mission duration in seconds
    
    # AI Settings
    MAX_AI_DEPTH: int = 3
    
    # dynamic parameters
    EVENT_SPAWN_RATE: float = 0.02
    OBSTACLE_SPAWN_RATE: float = 0.01

    # Terrain Types
    TERRAIN_TYPES: Tuple[str, ...] = ("plain", "forest", "water", "rock")
    
    # Visualization (disabled: web UI handles rendering via WebSocket)
    SHOW_VISUALIZATION: bool = False

    # Platform Settings
    API_HOST: str = environment.API_HOST
    API_PORT: int = environment.PORT
    LOG_LEVEL: str = environment.LOG_LEVEL

# Global config instance
settings = SimulationConfig()
