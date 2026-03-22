from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.simulation_engine import SimulationEngine
from services.mission_service.mission_service import MissionService
from services.swarm_service.swarm_service import SwarmService
from services.analytics_service.analytics_service import AnalyticsService
from controllers.mission_controller import MissionController
from monitoring.logging.logger import logger

# Initialize Engine and Services with safe fallback
engine = None
initialization_error = None

try:
    logger.info("Creating SimulationEngine...")
    engine = SimulationEngine()
    logger.info("Initializing SimulationEngine...")
    engine.initialize()
    logger.info("SimulationEngine initialized successfully.")
except Exception as e:
    initialization_error = str(e)
    logger.exception("Engine initialization failed (continuing in degraded mode): %s", e)
    try:
        logger.info("Attempting to create minimal engine stub...")
        engine = SimulationEngine()
        logger.info("Engine stub created.")
    except Exception as e2:
        logger.critical("Failed to create engine stub: %s", e2)
        # Create a mock engine object to prevent complete failure
        class MockEngine:
            def get_runtime_state(self):
                return {"error": "Engine failed to initialize", "detail": initialization_error}
        engine = MockEngine()
        logger.info("Using mock engine")

try:
    if hasattr(engine, 'initialize') and initialization_error is None:
        mission_service = MissionService(engine)
        swarm_service = SwarmService(engine)
        analytics_service = AnalyticsService(engine)
        mission_controller = MissionController(mission_service)
        logger.info("All services initialized successfully.")
    else:
        logger.warning("Services not fully initialized due to engine issues")
        mission_service = None
        swarm_service = None
        analytics_service = None
        mission_controller = None
except Exception as e:
    logger.exception("Service initialization failed: %s", e)
    mission_service = None
    swarm_service = None
    analytics_service = None
    mission_controller = None

app = FastAPI(title="AegisSwarm API", version="1.0.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Log startup event."""
    logger.info("✓ AegisSwarm API started successfully")
    logger.info(f"✓ Health check available at /health")
    logger.info(f"✓ WebSocket streaming available at /ws/simulation")

# Import routes after app and mission_controller are defined
from api.routes import mission, swarm, environment, analytics, health, stream

app.include_router(mission.router)
app.include_router(swarm.router)
app.include_router(environment.router)
app.include_router(analytics.router)
app.include_router(health.router)
app.include_router(stream.router)

@app.get("/")
async def root():
    """Root endpoint - simple health indicator for load balancers."""
    return {"status": "ok", "service": "AegisSwarm API", "version": "1.0.0"}
