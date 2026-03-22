from fastapi import APIRouter
from backend.api.server import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/coverage")
async def get_coverage():
    return {"coverage_percent": analytics_service.get_coverage()}

@router.get("/metrics")
async def get_metrics():
    return analytics_service.get_metrics()
