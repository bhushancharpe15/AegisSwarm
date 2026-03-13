from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["System"])

@router.get("")
async def health_check():
    """Returns the health status of the API."""
    return {
        "status": "ok",
        "service": "AegisSwarm API"
    }
