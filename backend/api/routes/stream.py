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
            try:
                if engine is None:
                    state = {"error": "Engine is not available", "status": "unavailable"}
                else:
                    state = engine.get_runtime_state()
                await websocket.send_text(json.dumps(state))
                await asyncio.sleep(0.2)  # Update rate
            except json.JSONDecodeError as je:
                logger.error(f"JSON encoding error: {je}")
                await asyncio.sleep(0.2)
            except Exception as se:
                logger.error(f"Send error: {se}")
                break
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass


