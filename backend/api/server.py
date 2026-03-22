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
try:
    logger.info("Creating SimulationEngine...")
    engine = SimulationEngine()
    logger.info("Initializing SimulationEngine...")
    engine.initialize()
    logger.info("SimulationEngine initialized successfully.")
except Exception as e:
    logger.exception("Engine initialization failed, running in degraded mode: %s", e)
    # Create a minimal engine stub to prevent crashes
    if engine is None:
        try:
            engine = SimulationEngine()
        except Exception as e2:
            logger.critical("Failed to create engine stub: %s", e2)
            raise

try:
    mission_service = MissionService(engine)
    swarm_service = SwarmService(engine)
    analytics_service = AnalyticsService(engine)
    mission_controller = MissionController(mission_service)
    logger.info("All services initialized successfully.")
except Exception as e:
    logger.exception("Service initialization failed: %s", e)
    raise

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
    """Verify critical components are ready on startup."""
    try:
        if engine is None:
            logger.critical("Engine is None on startup!")
            raise RuntimeError("Engine failed to initialize")
        logger.info("✓ Engine ready")
        if not hasattr(engine, 'state'):
            logger.critical("Engine missing state attribute!")
            raise RuntimeError("Engine state missing")
        logger.info("✓ Engine state accessible")
        logger.info("AegisSwarm API ready to accept requests")
    except Exception as e:
        logger.exception("Startup verification failed: %s", e)
        raise

# Import routes after app and mission_controller are defined
from api.routes import mission, swarm, environment, analytics, health, stream

app.include_router(mission.router)
app.include_router(swarm.router)
app.include_router(environment.router)
app.include_router(analytics.router)
app.include_router(health.router)
app.include_router(stream.router)
