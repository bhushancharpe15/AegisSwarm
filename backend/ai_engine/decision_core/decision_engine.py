from typing import Tuple, List, Dict, Any
from ai_engine.minimax.minimax_algorithm import MinimaxAlgorithm
from monitoring.logging.logger import logger

class DecisionEngine:
    """Encapsulates the decision-making logic for an individual robot."""
    
    def __init__(self, depth: int = 2):
        self.minimax = MinimaxAlgorithm(depth=depth)
        
    def choose_best_action(self, 
                           robot_id: str, 
                           current_pos: Tuple[int, int], 
                           environment: Any, 
                           other_robots_pos: List[Tuple[int, int]],
                           path_history: List[Tuple[int, int]],
                           sensor_range: int) -> Tuple[int, int]:
        """
        Analyzes the situation and returns the optimal next position.
        
        Args:
            robot_id: ID of the robot making the decision.
            current_pos: Current (x, y) coordinates of the robot.
            environment: The current environment state.
            other_robots_pos: Positions of other robots in the swarm.
            
        Returns:
            Tuple[int, int]: The chosen next (x, y) position.
        """
        logger.debug(f"Robot {robot_id} is calculating best move from {current_pos}...")
        
        optimal_pos = self.minimax.find_best_move(
            robot_id=robot_id,
            current_pos=current_pos,
            environment=environment,
            other_robots_pos=other_robots_pos,
            path_history=path_history,
            sensor_range=sensor_range,
        )

        frontier_pos = environment.get_next_step_towards_unexplored(current_pos, blocked_positions=other_robots_pos)
        recent_positions = path_history[-6:]
        is_oscillating = len(recent_positions) >= 4 and len(set(recent_positions)) <= 3
        optimal_gain = environment.estimate_exploration_gain(optimal_pos[0], optimal_pos[1], sensor_range)

        if frontier_pos != current_pos and (optimal_pos == current_pos or optimal_gain == 0 or is_oscillating):
            logger.debug(f"Robot {robot_id} switching to frontier move {frontier_pos} from {current_pos}")
            return frontier_pos
        
        logger.debug(f"Robot {robot_id} selected move to {optimal_pos}")
        return optimal_pos
