from services.mission_service.mission_service import MissionService
from monitoring.logging.logger import logger

class MissionController:
    def __init__(self, mission_service: MissionService):
        self.service = mission_service

    def start(self):
        logger.info("Controller: Starting mission")
        self.service.start_mission()
        return {"status": "success", "message": "Mission started"}

    def pause(self):
        self.service.pause_mission()
        return {"status": "success", "message": "Mission paused"}

    def resume(self):
        self.service.resume_mission()
        return {"status": "success", "message": "Mission resumed"}

    def stop(self):
        self.service.stop_mission()
        return {"status": "success", "message": "Mission stopped"}

    def reset(self):
        self.service.reset_mission()
        return {"status": "success", "message": "Mission reset"}

    def status(self):
        return self.service.get_status()
