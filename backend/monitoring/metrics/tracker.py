from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class SimulationMetrics:
    """Tracks system metrics for the AegisSwarm simulation."""
    
    robots_active: int = 0
    collisions_detected: int = 0
    cells_explored: int = 0
    simulation_steps: int = 0
    energy_consumed: float = 0.0
    
    def reset(self):
        """Resets all metrics to zero."""
        self.robots_active = 0
        self.collisions_detected = 0
        self.cells_explored = 0
        self.simulation_steps = 0
        self.energy_consumed = 0.0
        
    def to_dict(self) -> Dict[str, Any]:
        """Returns metrics as a dictionary."""
        return {
            "robots_active": self.robots_active,
            "collisions_detected": self.collisions_detected,
            "cells_explored": self.cells_explored,
            "simulation_steps": self.simulation_steps,
            "energy_consumed": self.energy_consumed
        }

    def __str__(self) -> str:
        return (f"Simulation Metrics: Steps={self.simulation_steps}, "
                f"Active Robots={self.robots_active}, "
                f"Collisions={self.collisions_detected}, "
                f"Explored={self.cells_explored}")

# Global metrics tracker
metrics = SimulationMetrics()
