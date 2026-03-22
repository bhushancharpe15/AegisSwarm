from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.server import swarm_service

router = APIRouter(prefix="/robots", tags=["Swarm"])

@router.get("/status")
async def get_swarm_status():
    if swarm_service is None:
        return JSONResponse({"error": "Swarm service not initialized", "status": "unavailable"}, status_code=503)
    return swarm_service.get_swarm_status()

@router.get("/positions")
async def get_robot_positions():
    if swarm_service is None:
        return JSONResponse({"error": "Swarm service not initialized", "status": "unavailable"}, status_code=503)
    return swarm_service.get_robot_positions()

@router.get("/active")
async def get_active_count():
    if swarm_service is None:
        return JSONResponse({"error": "Swarm service not initialized", "status": "unavailable"}, status_code=503)
    return {"active_robots": swarm_service.get_active_robots()}
