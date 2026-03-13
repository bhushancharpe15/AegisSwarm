from typing import Dict, Any, List
frommonitoring.logging.logger import logger

class SwarmCommunication:
    """Basic swarm communication protocol for sharing discoveries."""
    
    def __init__(self):
        self.shared_knowledge = {
            "obstacles": [],
            "events": [],
            "terrain_warnings": []
        }

    def broadcast_discovery(self, robot_id: str, discovery_type: str, data: Any):
        """Broadcasts a discovery to the swarm."""
        if discovery_type in self.shared_knowledge:
            if data not in self.shared_knowledge[discovery_type]:
                self.shared_knowledge[discovery_type].append(data)
                logger.info(f"Swarm Broadcast: Robot {robot_id} found {discovery_type} at {data}")
                return True
        return False

    def get_shared_knowledge(self) -> Dict[str, List[Any]]:
        """Returns all shared knowledge."""
        return self.shared_knowledge
