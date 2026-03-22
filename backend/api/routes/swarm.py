from fastapi import APIRouter
from api.server import swarm_service

router = APIRouter(prefix="/robots", tags=["Swarm"])

@router.get("/status")
async def get_swarm_status():
    return swarm_service.get_swarm_status()

@router.get("/positions")
async def get_robot_positions():
    return swarm_service.get_robot_positions()

@router.get("/active")
async def get_active_count():
    return {"active_robots": swarm_service.get_active_robots()}
