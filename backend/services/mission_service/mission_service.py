from typing import Dict, Any
fromcore.simulation_engine import SimulationEngine, MissionState
frommonitoring.logging.logger import logger

class MissionService:
    def __init__(self, engine: SimulationEngine):
        self.engine = engine

    def start_mission(self):
        self.engine.start()

    def pause_mission(self):
        self.engine.pause()

    def resume_mission(self):
        self.engine.resume()

    def reset_mission(self):
        self.engine.reset()

    def stop_mission(self):
        self.engine.stop()

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.engine.state.value,
            "step_count": self.engine.step_count
        }
