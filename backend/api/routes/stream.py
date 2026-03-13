import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.server import engine
from monitoring.logging.logger import logger

router = APIRouter(tags=["Streaming"])

@router.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established for simulation streaming.")
    try:
        while True:
            state = engine.get_runtime_state()
            await websocket.send_text(json.dumps(state))
            await asyncio.sleep(0.2) # Update rate
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()


