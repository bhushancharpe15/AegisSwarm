# AegisSwarm System Architecture

AegisSwarm follows a layered architecture that separates API concerns, simulation runtime, swarm intelligence, and presentation.

## Layered Design

### 1. Presentation Layer (Frontend)
The React dashboard provides mission controls and live state visualization.
- Consumes REST endpoints for mission commands and metrics.
- Consumes WebSocket updates from `/ws/simulation` for real-time rendering.

### 2. API Layer (FastAPI)
The API layer exposes control and telemetry interfaces.
- Route modules under `backend/api/routes` define mission, swarm, environment, analytics, health, and stream endpoints.
- CORS middleware is configured for cross-origin frontend access.
- Health endpoint (`GET /health`) provides platform readiness status.

### 3. Application Services Layer
Service modules coordinate use-cases between API routes and the simulation core.
- `MissionService` controls lifecycle actions.
- `SwarmService` provides robot state and control operations.
- `AnalyticsService` exposes mission analytics and metrics.

### 4. Core Simulation Layer
`SimulationEngine` is the runtime authority for mission progression.
- Initializes and manages environment and swarm instances.
- Runs mission loop and tracks mission state.
- Publishes runtime state consumed by API/WebSocket routes.

### 5. Swarm Intelligence Layer
Robotic agents make local decisions while sharing discoveries.
- Heuristic and minimax modules evaluate candidate actions.
- Swarm communication protocol supports distributed coordination.

### 6. Environment Layer
Environment modules model terrain, grid occupancy, events, and obstacles.
- Grid and terrain managers provide map semantics.
- Obstacle/event systems introduce dynamic environmental conditions.

## Runtime and Deployment Model

### API Startup
Production startup is uvicorn-first and cloud-compatible:

```bash
uvicorn backend.api.server:app --host 0.0.0.0 --port $PORT
```

### Environment Configuration
Environment variables are loaded from `backend/config/environment.py`.
- `PORT`
- `API_HOST`
- `LOG_LEVEL`

### Cloud Readiness (Railway)
- Dynamic port binding through `PORT`.
- Cross-origin API access enabled via CORS.
- WebSocket streaming available across domains at `/ws/simulation`.
- Health checks supported via `/health`.

## Request and State Flow
1. Frontend sends mission command to REST endpoint.
2. API route delegates operation to a service.
3. Service invokes `SimulationEngine` state transition.
4. Engine advances simulation and updates metrics/state.
5. WebSocket route streams current runtime state to clients.
6. Frontend renders updated mission and swarm state.
