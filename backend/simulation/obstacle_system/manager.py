import random
from typing import List, Tuple, Set
import numpy as np

class ObstacleManager:
    """Handles static and dynamic obstacles within the simulation environment."""
    
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size
        self.static_obstacles: Set[Tuple[int, int]] = set()
        self.dynamic_obstacles: Set[Tuple[int, int]] = set()
        self.hazard_zones: Set[Tuple[int, int]] = set()
        
    def add_obstacle(self, x: int, y: int, is_static: bool = True):
        """Adds an obstacle at a given location."""
        if is_static:
            self.static_obstacles.add((x, y))
        else:
            self.dynamic_obstacles.add((x, y))
            
    def remove_obstacle(self, x: int, y: int):
        """Removes an obstacle from a location."""
        self.static_obstacles.discard((x, y))
        self.dynamic_obstacles.discard((x, y))
        
    def generate_random_obstacles(self, density: float):
        """Generates random static obstacles across the grid based on density."""
        num_cells = self.grid_size[0] * self.grid_size[1]
        num_obstacles = int(num_cells * density)

        self.static_obstacles.clear()
        self.dynamic_obstacles.clear()
        self.hazard_zones.clear()

        while len(self.static_obstacles) < num_obstacles:
            x = random.randint(0, self.grid_size[0] - 1)
            y = random.randint(0, self.grid_size[1] - 1)
            self.add_obstacle(x, y)
            
    def is_obstacle(self, x: int, y: int) -> bool:
        """Checks if a given cell has an obstacle."""
        return (x, y) in self.static_obstacles or (x, y) in self.dynamic_obstacles
    
    def detect_collision(self, x: int, y: int) -> bool:
        """Detecst if a position results in a collision."""
        if not (0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]):
            return True # Edge of world is a collision
        return self.is_obstacle(x, y)
