from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.simulation_engine import SimulationEngine
from services.mission_service.mission_service import MissionService
from services.swarm_service.swarm_service import SwarmService
from services.analytics_service.analytics_service import AnalyticsService
from controllers.mission_controller import MissionController

# Initialize Engine and Services
engine = SimulationEngine()
engine.initialize()

mission_service = MissionService(engine)
swarm_service = SwarmService(engine)
analytics_service = AnalyticsService(engine)

mission_controller = MissionController(mission_service)

app = FastAPI(title="AegisSwarm API", version="1.0.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes after app and mission_controller are defined
from api.routes import mission, swarm, environment, analytics, health, stream

app.include_router(mission.router)
app.include_router(swarm.router)
app.include_router(environment.router)
app.include_router(analytics.router)
app.include_router(health.router)
app.include_router(stream.router)
