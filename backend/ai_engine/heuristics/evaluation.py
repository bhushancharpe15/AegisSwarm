from typing import Tuple, Dict, List, Any
import numpy as np
from monitoring.logging.logger import logger

class HeuristicEvaluator:
    """Provides scoring logic for evaluating environment states from a robot's perspective."""
    
    # Configurable Scoring Constants
    UNEXPLORED_BONUS = 10.0
    EVENT_BONUS = 15.0  # Increased
    EVENT_PROXIMITY_BONUS = 5.0
    OBSTACLE_PENALTY = -12.0 # Increased
    COLLISION_PENALTY = -20.0 # Increased
    ALREADY_EXPLORED_PENALTY = -5.0 # Increased
    
    @staticmethod
    def evaluate_state(robot_id: str, 
                       position: Tuple[int, int], 
                       environment: Any, 
                       other_robots_pos: List[Tuple[int, int]],
                       path_history: List[Tuple[int, int]] = None,
                       current_pos: Tuple[int, int] = None) -> float:
        """
        Evaluate the score of a robot being at a specific position.
        """
        x, y = position
        score = 0.0
        
        # 1. Boundary Check
        if not (0 <= x < environment.width and 0 <= y < environment.height):
            return -1000.0 # Extreme penalty for out of bounds
            
        # 2. Obstacle Proximity/Collision
        if environment.obstacle_manager.is_obstacle(x, y):
            score += HeuristicEvaluator.OBSTACLE_PENALTY
            
        # 3. Collision with other robots
        if position in other_robots_pos:
            score += HeuristicEvaluator.COLLISION_PENALTY
            
        # 4. Terrain Movement Cost
        move_cost = environment.terrain_manager.get_movement_cost(x, y)
        score -= (move_cost * 2.0) # Penalty for difficult terrain
        
        # 5. Exploration Logic
        if hasattr(environment, 'explored_mask'):
            if not environment.explored_mask[x, y]:
                score += HeuristicEvaluator.UNEXPLORED_BONUS
            else:
                score += HeuristicEvaluator.ALREADY_EXPLORED_PENALTY

        # 5.5 Movement quality: penalize staying still, immediate backtracking, and repeated visits.
        if current_pos is not None and position == current_pos:
            score -= 3.0

        if path_history:
            visit_count = path_history.count(position)
            score -= visit_count * 1.75

            if len(path_history) >= 2 and position == path_history[-2]:
                score -= 8.0
        
        # 6. Environmental Events
        if (x, y) in environment.events:
            score += HeuristicEvaluator.EVENT_BONUS
            
        # 7. Proximity to unexplored territory (Gradient scent)
        # Search in a small radius for unexplored cells to encourage movement towards them
        unexplored_nearby = 0
        search_radius = 2
        for dx in range(-search_radius, search_radius + 1):
            for dy in range(-search_radius, search_radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < environment.width and 0 <= ny < environment.height:
                    if hasattr(environment, 'explored_mask') and not environment.explored_mask[nx, ny]:
                        unexplored_nearby += 1
        
        score += (unexplored_nearby * 0.5)

        # Prefer cells on the frontier between explored and unexplored space.
        frontier_bonus = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < environment.width and 0 <= ny < environment.height:
                if hasattr(environment, 'explored_mask') and not environment.explored_mask[nx, ny]:
                    frontier_bonus += 1

        score += frontier_bonus * 1.5
        
        return score
