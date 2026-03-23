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
                
                # Ensure state is JSON serializable
                if not isinstance(state, dict):
                    state = {"data": str(state)}
                
                await websocket.send_text(json.dumps(state))
                await asyncio.sleep(0.2)  # Update rate
            except json.JSONDecodeError as je:
                logger.error(f"JSON encoding error: {je}")
                await asyncio.sleep(0.2)
            except Exception as se:
                logger.exception(f"Send error in WebSocket: {type(se).__name__}: {se}")
                break
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed by client.")
    except Exception as e:
        logger.exception(f"WebSocket error: {type(e).__name__}: {e}")
        try:
            await websocket.close()
        except:
            pass


