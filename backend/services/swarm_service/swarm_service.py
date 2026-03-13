from typing import List, Dict, Any
fromcore.simulation_engine import SimulationEngine

class SwarmService:
    def __init__(self, engine: SimulationEngine):
        self.engine = engine

    def get_active_robots(self) -> int:
        return len([r for r in self.engine.swarm_mgr.robots.values() if r.status == "active"])

    def get_robot_positions(self) -> Dict[str, Any]:
        return {rid: r.position for rid, r in self.engine.swarm_mgr.robots.items()}

    def get_swarm_status(self) -> List[Dict[str, Any]]:
        return self.engine.swarm_mgr.track_swarm_state()
