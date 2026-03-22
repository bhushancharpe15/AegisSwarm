from typing import List, Dict, Tuple, Any
import random
from backend.swarm.robot_agent.agent import RobotAgent
from backend.monitoring.logging.logger import logger
from backend.monitoring.metrics.tracker import metrics

from backend.swarm.communication.protocol import SwarmCommunication

class SwarmManager:
    """Manages and coordinates a collection of RobotAgents."""
    
    def __init__(self):
        self.robots: Dict[str, RobotAgent] = {}
        self.comm_hub = SwarmCommunication()
        
    def initialize_swarm(self, num_robots: int, grid_size: Tuple[int, int], sensor_range: int, energy_level: float, environment: Any):
        """Spawns multiple robots at random valid positions."""
        self.robots.clear()
        self.comm_hub = SwarmCommunication() # Reset comms
        occupied_positions = set()

        for i in range(num_robots):
            robot_id = f"R-{i:03d}"
            pos = None
            for _ in range(grid_size[0] * grid_size[1] * 2):
                candidate = (random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1))
                if candidate not in occupied_positions and environment.is_valid_position(*candidate):
                    pos = candidate
                    occupied_positions.add(candidate)
                    break

            if pos is None:
                raise ValueError("Unable to place robots on valid unique positions")

            self.add_robot(robot_id, pos, sensor_range, energy_level, 1.0)
            
        logger.info(f"Swarm initialized with {num_robots} robots.")
        metrics.robots_active = num_robots
        
    def add_robot(self, robot_id: str, position: Tuple[int, int], sensor_range: int, energy_level: float, speed: float):
        """Adds a new robot to the swarm tracker with communication hub access."""
        robot = RobotAgent(robot_id, position, sensor_range, energy_level, speed, comm_hub=self.comm_hub)
        self.robots[robot_id] = robot
        
    def remove_robot(self, robot_id: str):
        """Removes a robot from the swarm tracker."""
        if robot_id in self.robots:
            del self.robots[robot_id]
            metrics.robots_active = len(self.robots)
            
    def update_robot_positions(self, environment: Any):
        """Updates positions of all robots using basic random movement (Phase 1)."""
        directions = ['up', 'down', 'left', 'right', 'stay']
        
        occupied_positions = {r.position for r in self.robots.values()}
        
        for robot_id, robot in self.robots.items():
            if robot.status != "active":
                continue
                
            move = random.choice(directions)
            new_pos = robot.position
            
            if move == 'up': new_pos = robot.move_up()
            elif move == 'down': new_pos = robot.move_down()
            elif move == 'left': new_pos = robot.move_left()
            elif move == 'right': new_pos = robot.move_right()
            
            # Simple collision avoidance and boundary checks
            if environment.is_valid_position(*new_pos) and new_pos not in occupied_positions:
                robot.update_position(new_pos)
            else:
                if environment.obstacle_manager.is_obstacle(*new_pos):
                    metrics.collisions_detected += 1
                    logger.debug(f"Robot {robot_id} attempted to move into obstacle at {new_pos}")
                # Else: boundary or other robot, just stay put
                
            robot.update_state()
            
    def track_swarm_state(self) -> List[Dict[str, Any]]:
        """Returns the collective state of the swarm."""
        return [robot.get_state() for robot in self.robots.values()]
