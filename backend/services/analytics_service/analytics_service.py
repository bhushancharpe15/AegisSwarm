import numpy as np
from typing import Dict, Any
from backend.core.simulation_engine import SimulationEngine
from backend.monitoring.metrics.tracker import metrics

class AnalyticsService:
    def __init__(self, engine: SimulationEngine):
        self.engine = engine

    def get_coverage(self) -> float:
        total_cells = self.engine.env.width * self.engine.env.height
        explored_cells = np.sum(self.engine.env.explored_mask)
        return (explored_cells / total_cells) * 100

    def get_metrics(self) -> Dict[str, Any]:
        m_dict = metrics.to_dict()
        m_dict["coverage_percent"] = float(self.get_coverage())
        m_dict["events_detected"] = len(self.engine.swarm_mgr.comm_hub.get_shared_knowledge().get("events", []))
        return m_dict
