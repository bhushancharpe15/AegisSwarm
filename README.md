# AegisSwarm

AegisSwarm is a swarm simulation platform for environmental exploration with a FastAPI backend and a React dashboard.

## Overview
- Real-time simulation engine with mission lifecycle control.
- Swarm decision logic powered by heuristics and minimax.
- REST API for control and analytics.
- WebSocket stream for live simulation state updates.
- Railway-ready backend deployment configuration.

## Repository Layout
- `backend/`: FastAPI API, simulation core, AI logic, services, monitoring.
- `frontend/`: React + Vite dashboard.
- `docs/`: architecture and technical documentation.

## Backend Development

### Requirements
- Python 3.10+

### Install
```bash
cd backend
pip install -r requirements.txt
```

### Run API (local)
```bash
uvicorn backend.api.server:app --host 0.0.0.0 --port 8000
```

Alternative entrypoint:
```bash
python backend/main.py --server
```

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "ok",
  "service": "AegisSwarm API"
}
```

### WebSocket Stream
```text
WS /ws/simulation
```

## Frontend Development

### Install
```bash
cd frontend
npm install
```

### Run
```bash
npm run dev
```

## Environment Variables

Backend supports the following environment variables:
- `PORT`: API port (defaults to `8000`).
- `API_HOST`: bind host (defaults to `0.0.0.0`).
- `LOG_LEVEL`: logger level (defaults to `INFO`).

`python-dotenv` is included, so values can be supplied via environment or `.env`.

## Railway Deployment

Use this start command on Railway:

```bash
uvicorn backend.api.server:app --host 0.0.0.0 --port $PORT
```

Deployment notes:
- Backend binds to Railway dynamic `PORT`.
- CORS is enabled for cross-origin frontend access.
- WebSocket endpoint is available for cross-domain clients.
- `/health` endpoint is ready for platform health checks.

## API Surface
- `GET /health`
- `POST /mission/start`
- `POST /mission/pause`
- `POST /mission/stop`
- `GET /analytics/metrics`
- `WS /ws/simulation`

## Architecture
See [docs/architecture.md](docs/architecture.md).
