from fastapi import APIRouter
from monitoring.logging.logger import logger

router = APIRouter(prefix="/health", tags=["System"])

@router.get("")
async def health_check():
    """Returns the health status of the API."""
    try:
        logger.debug("Health check requested")
        return {
            "status": "ok",
            "service": "AegisSwarm API"
        }
    except Exception as e:
        logger.exception("Health check failed: %s", e)
        return {
            "status": "error",
            "service": "AegisSwarm API",
            "error": str(e)
        }, 500
