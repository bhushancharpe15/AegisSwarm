from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.server import engine

router = APIRouter(prefix="/environment", tags=["Environment"])

@router.get("/grid")
async def get_grid():
    if engine is None or not hasattr(engine, 'env'):
        return JSONResponse({"error": "Engine not initialized", "status": "unavailable"}, status_code=503)
    return engine.env.get_environment_state()

@router.post("/add_obstacle")
async def add_obstacle(x: int, y: int):
    if engine is None or not hasattr(engine, 'env'):
        return JSONResponse({"error": "Engine not initialized", "status": "unavailable"}, status_code=503)
    engine.env.obstacle_manager.add_obstacle(x, y)
    engine.env.update_environment()
    return {"status": "success", "message": f"Obstacle added at ({x}, {y})"}

@router.post("/add_event")
async def add_event(x: int, y: int):
    if engine is None or not hasattr(engine, 'env'):
        return JSONResponse({"error": "Engine not initialized", "status": "unavailable"}, status_code=503)
    engine.env.events.append((x, y))
    engine.env.update_environment()
    return {"status": "success", "message": f"Event added at ({x}, {y})"}
