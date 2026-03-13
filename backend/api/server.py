from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
fromcore.simulation_engine import SimulationEngine
fromservices.mission_service.mission_service import MissionService
fromservices.swarm_service.swarm_service import SwarmService
fromservices.analytics_service.analytics_service import AnalyticsService
fromcontrollers.mission_controller import MissionController

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
fromapi.routes import mission, swarm, environment, analytics, health, stream

app.include_router(mission.router)
app.include_router(swarm.router)
app.include_router(environment.router)
app.include_router(analytics.router)
app.include_router(health.router)
app.include_router(stream.router)
