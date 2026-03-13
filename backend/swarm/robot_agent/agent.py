from typing import Tuple, List, Dict, Any
frommonitoring.logging.logger import logger
frommonitoring.metrics.tracker import metrics
fromai_engine.decision_core.decision_engine import DecisionEngine
fromconfig.settings import settings

class RobotAgent:
    """Represents an individual robotic agent in the swarm."""
    
    def __init__(self, robot_id: str, position: Tuple[int, int], sensor_range: int, energy_level: float, movement_speed: float, comm_hub=None):
        self.robot_id = robot_id
        self.position = position
        self.sensor_range = sensor_range
        self.energy_level = energy_level
        self.movement_speed = movement_speed
        self.comm_hub = comm_hub
        self.status = "active"
        self.path_history: List[Tuple[int, int]] = [position]
        
        # Phase 2: AI Decision Engine
        self.decision_engine = DecisionEngine(depth=settings.MAX_AI_DEPTH)
        
    def move(self, new_position: Tuple[int, int]):
        """Executes a move to a new position."""
        self.update_position(new_position)

    def move_up(self) -> Tuple[int, int]:
        return (self.position[0], self.position[1] - 1)
        
    def move_down(self) -> Tuple[int, int]:
        return (self.position[0], self.position[1] + 1)
        
    def move_left(self) -> Tuple[int, int]:
        return (self.position[0] - 1, self.position[1])
        
    def move_right(self) -> Tuple[int, int]:
        return (self.position[0] + 1, self.position[1])
        
    def update_position(self, new_position: Tuple[int, int]):
        """Updates the robot's position and tracks history."""
        old_position = self.position
        self.position = new_position
        self.path_history.append(new_position)
        self.energy_level -= 0.5 # Basic energy consumption
        metrics.energy_consumed += 0.5
        
        logger.debug(f"Robot {self.robot_id} moved from {old_position} to {new_position}")
        
    def scan_environment(self, environment: Any) -> List[Tuple[int, int, str]]:
        """Scans the surrounding environment within sensor range."""
        visible_cells = []
        x_range = range(max(0, self.position[0] - self.sensor_range), 
                        min(environment.width, self.position[0] + self.sensor_range + 1))
        y_range = range(max(0, self.position[1] - self.sensor_range), 
                        min(environment.height, self.position[1] + self.sensor_range + 1))
        
        for x in x_range:
            for y in y_range:
                cell_type = environment.grid[x, y]
                visible_cells.append((x, y, cell_type))
                
        logger.debug(f"Robot {self.robot_id} scanned {len(visible_cells)} cells around {self.position}")
        
        # Swarm Communication: Broadcast discoveries
        for x, y, cell_type in visible_cells:
            if cell_type == 'F': # Event found
                self.broadcast('events', (x, y))
            elif cell_type == 'X': # Obstacle found
                self.broadcast('obstacles', (x, y))
                
        return visible_cells

    def broadcast(self, discovery_type: str, data: Any):
        """Broadcasts a discovery to the swarm communication hub."""
        if self.comm_hub:
            self.comm_hub.broadcast_discovery(self.robot_id, discovery_type, data)

    def update_state(self):
        """Updates internal state and status."""
        if self.energy_level <= 0:
            self.status = "depleted"
            logger.warning(f"Robot {self.robot_id} energy depleted!")
        
    def get_state(self) -> Dict[str, Any]:
        """Returns the current state of the robot."""
        return {
            "robot_id": self.robot_id,
            "position": self.position,
            "energy_level": self.energy_level,
            "status": self.status
        }
