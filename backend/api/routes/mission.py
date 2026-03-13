from fastapi import APIRouter
from api.server import mission_controller

router = APIRouter(prefix="/mission", tags=["Mission"])

@router.post("/start")
async def start_mission():
    return mission_controller.start()

@router.post("/pause")
async def pause_mission():
    return mission_controller.pause()

@router.post("/resume")
async def resume_mission():
    return mission_controller.resume()

@router.post("/stop")
async def stop_mission():
    return mission_controller.stop()

@router.post("/reset")
async def reset_mission():
    return mission_controller.reset()

@router.get("/status")
async def get_status():
    return mission_controller.status()
