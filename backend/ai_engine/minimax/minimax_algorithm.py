from typing import Tuple, List, Dict, Any, Callable
import copy
import numpy as np
fromai_engine.heuristics.evaluation import HeuristicEvaluator
frommonitoring.logging.logger import logger

class MinimaxAlgorithm:
    """Implement Minimax search with Alpha-Beta pruning."""
    
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.evaluator = HeuristicEvaluator()
        
    def find_best_move(self, 
                       robot_id: str, 
                       current_pos: Tuple[int, int], 
                       environment: Any, 
                       other_robots_pos: List[Tuple[int, int]],
                       path_history: List[Tuple[int, int]],
                       sensor_range: int) -> Tuple[int, int]:
        best_score = float('-inf')
        best_move = current_pos
        alpha = float('-inf')
        beta = float('inf')
        
        possible_moves = [(current_pos[0], current_pos[1]-1), (current_pos[0], current_pos[1]+1),
                          (current_pos[0]-1, current_pos[1]), (current_pos[0]+1, current_pos[1]),
                          current_pos]
        
        valid_moves = [m for m in possible_moves if environment.is_valid_position(*m) and m not in other_robots_pos]

        if not valid_moves:
            return current_pos
        
        for move in valid_moves:
            simulated_env = self.simulate_future_state(environment, move, sensor_range)
            
            score = self._minimax(move, self.depth - 1, False, alpha, beta, 
                                 robot_id, simulated_env, other_robots_pos, path_history + [move], sensor_range, current_pos)
            
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            
        return best_move

    def simulate_future_state(self, environment: Any, move: Tuple[int, int], sensor_range: int) -> Any:
        """Simulates the environment state after a specific move using deepcopy."""
        sim_env = copy.deepcopy(environment)
        sim_env.mark_explored(move[0], move[1], sensor_range)
        return sim_env

    def _minimax(self, 
                 position: Tuple[int, int], 
                 depth: int, 
                 is_maximizing: bool, 
                 alpha: float, 
                 beta: float,
                 robot_id: str,
                 environment: Any,
                 other_robots_pos: List[Tuple[int, int]],
                 path_history: List[Tuple[int, int]],
                 sensor_range: int,
                 origin_pos: Tuple[int, int]) -> float:
        """Recursive minimax function with simulated state lookahead."""
        if depth == 0:
            return self.evaluator.evaluate_state(
                robot_id,
                position,
                environment,
                other_robots_pos,
                path_history=path_history,
                current_pos=origin_pos,
            )
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in self._get_adjacent_moves(position, environment):
                sim_env = self.simulate_future_state(environment, move, sensor_range)
                eval = self._minimax(move, depth - 1, False, alpha, beta, 
                                    robot_id, sim_env, other_robots_pos, path_history + [move], sensor_range, origin_pos)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self._get_adjacent_moves(position, environment):
                sim_env = self.simulate_future_state(environment, move, sensor_range)
                eval = self._minimax(move, depth - 1, True, alpha, beta, 
                                    robot_id, sim_env, other_robots_pos, path_history + [move], sensor_range, origin_pos)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _get_adjacent_moves(self, pos: Tuple[int, int], environment: Any) -> List[Tuple[int, int]]:
        x, y = pos
        moves = [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x, y)]
        return [m for m in moves if environment.is_valid_position(*m)]
