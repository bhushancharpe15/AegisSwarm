from fastapi import APIRouter
from backend.api.server import engine

router = APIRouter(prefix="/environment", tags=["Environment"])

@router.get("/grid")
async def get_grid():
    return engine.env.get_environment_state()

@router.post("/add_obstacle")
async def add_obstacle(x: int, y: int):
    engine.env.obstacle_manager.add_obstacle(x, y)
    engine.env.update_environment()
    return {"status": "success", "message": f"Obstacle added at ({x}, {y})"}

@router.post("/add_event")
async def add_event(x: int, y: int):
    engine.env.events.append((x, y))
    engine.env.update_environment()
    return {"status": "success", "message": f"Event added at ({x}, {y})"}
