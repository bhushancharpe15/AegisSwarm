import numpy as np
from collections import deque
from typing import Tuple, Dict, Any, List
from simulation.terrain.terrain_manager import TerrainManager
from simulation.obstacle_system.manager import ObstacleManager
from monitoring.logging.logger import logger
from config.settings import settings

class Environment:
    """Core simulation environment, managing the grid, terrain, and obstacles."""
    
    # Cell Representation
    EMPTY = '.'
    OBSTACLE = 'X'
    EVENT = 'F'
    ROBOT = 'R'
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.full((width, height), self.EMPTY, dtype='<U1')
        self.terrain_manager = TerrainManager((width, height))
        self.obstacle_manager = ObstacleManager((width, height))
        self.events: List[Tuple[int, int]] = []
        
        # Phase 2: Exploration Tracking
        self.explored_mask = np.zeros((width, height), dtype=bool)
        self.heatmap_grid = np.zeros((width, height), dtype=int) # 0: unexplored, 1: partial, 2: full
        
        logger.info(f"Environment initialized with grid size: {width}x{height}")
        
    def generate_grid(self, obstacle_density: float, event_density: float):
        """Initializes the environment with terrain, obstacles, and events."""
        self.grid.fill(self.EMPTY)
        self.events = []
        self.explored_mask.fill(False)
        self.heatmap_grid.fill(0)
        self.terrain_manager.generate_random_terrain()
        self.obstacle_manager.generate_random_obstacles(obstacle_density)
        self.place_events(event_density)
        self.update_environment()
        
    def mark_explored(self, x: int, y: int, radius: int):
        """Marks cells within a radius as explored and updates heatmap intensity."""
        x_min, x_max = max(0, x - radius), min(self.width, x + radius + 1)
        y_min, y_max = max(0, y - radius), min(self.height, y + radius + 1)
        self.explored_mask[x_min:x_max, y_min:y_max] = True
        
        # Update heatmap: increment intensity up to 2
        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if self.heatmap_grid[i, j] < 2:
                    self.heatmap_grid[i, j] += 1
        
    def place_events(self, density: float):
        """Randomly places environmental events."""
        num_cells = self.width * self.height
        num_events = int(num_cells * density)
        while len(self.events) < num_events:
            x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            if not self.obstacle_manager.is_obstacle(x, y) and (x, y) not in self.events:
                self.events.append((x, y))
                
    def update_environment(self):
        """Updates the grid display representation."""
        # Reset grid from base representation
        self.grid.fill(self.EMPTY)
        
        # Add obstacles
        for x, y in self.obstacle_manager.static_obstacles:
            self.grid[x, y] = self.OBSTACLE
        for x, y in self.obstacle_manager.dynamic_obstacles:
            self.grid[x, y] = self.OBSTACLE
            
        # Add events
        for x, y in self.events:
            if self.grid[x, y] == self.EMPTY:
                self.grid[x, y] = self.EVENT
                
    def get_environment_state(self) -> Dict[str, Any]:
        """Returns the current state of the environment."""
        return {
            "grid": self.grid.tolist(),
            "static_obstacles": list(self.obstacle_manager.static_obstacles),
            "events": self.events,
            "heatmap": self.heatmap_grid.tolist()
        }
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Checks if a position is within grid bounds and not an obstacle."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return not self.obstacle_manager.is_obstacle(x, y)

    def get_valid_neighbors(self, x: int, y: int, blocked_positions=None) -> List[Tuple[int, int]]:
        blocked = set(blocked_positions or [])
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [pos for pos in neighbors if self.is_valid_position(*pos) and pos not in blocked]

    def estimate_exploration_gain(self, x: int, y: int, radius: int) -> int:
        x_min, x_max = max(0, x - radius), min(self.width, x + radius + 1)
        y_min, y_max = max(0, y - radius), min(self.height, y + radius + 1)
        return int(np.sum(~self.explored_mask[x_min:x_max, y_min:y_max]))

    def get_next_step_towards_unexplored(self, start: Tuple[int, int], blocked_positions=None) -> Tuple[int, int]:
        blocked = set(blocked_positions or [])
        blocked.discard(start)

        queue = deque([(start, None)])
        visited = {start}

        while queue:
            current, first_step = queue.popleft()
            x, y = current

            if current != start and not self.explored_mask[x, y]:
                return first_step or current

            for neighbor in self.get_valid_neighbors(x, y, blocked_positions=blocked):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append((neighbor, neighbor if first_step is None else first_step))

        return start
