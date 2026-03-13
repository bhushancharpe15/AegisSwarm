import random
from typing import Dict, Any, Tuple
import numpy as np

class TerrainManager:
    """Manages terrain types and their properties for the simulation grid."""
    
    TERRAIN_PROPERTIES: Dict[str, Dict[str, Any]] = {
        "plain": {"move_cost": 1.0, "color": "#90ee90"},  # LightGreen
        "forest": {"move_cost": 2.5, "color": "#228b22"}, # ForestGreen
        "water": {"move_cost": 5.0, "color": "#1e90ff"},  # DodgerBlue
        "rock": {"move_cost": 3.5, "color": "#808080"}    # Gray
    }
    
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size
        self.terrain_grid = np.full(grid_size, "plain", dtype=object)
        
    def generate_random_terrain(self):
        """Generates random terrain types across the grid."""
        terrain_types = list(self.TERRAIN_PROPERTIES.keys())
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # 80% chance of staying plain, 20% for others for a more natural look
                if random.random() < 0.2:
                    self.terrain_grid[i][j] = random.choice(terrain_types)
                else:
                    self.terrain_grid[i][j] = "plain"
                    
    def get_terrain_at(self, x: int, y: int) -> str:
        """Returns the terrain type at a given position."""
        return self.terrain_grid[x][y]
    
    def get_movement_cost(self, x: int, y: int) -> float:
        """Returns the movement cost for the terrain at a given position."""
        terrain_type = self.get_terrain_at(x, y)
        return self.TERRAIN_PROPERTIES[terrain_type]["move_cost"]
