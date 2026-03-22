from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.server import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/coverage")
async def get_coverage():
    if analytics_service is None:
        return JSONResponse({"error": "Analytics service not initialized", "status": "unavailable"}, status_code=503)
    return {"coverage_percent": analytics_service.get_coverage()}

@router.get("/metrics")
async def get_metrics():
    if analytics_service is None:
        return JSONResponse({"error": "Analytics service not initialized", "status": "unavailable"}, status_code=503)
    return analytics_service.get_metrics()
