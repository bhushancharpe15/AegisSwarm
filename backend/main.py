import argparse
import os
import uvicorn
from core.simulation_engine import SimulationEngine
from monitoring.logging.logger import logger

def run_local_simulation():
    """Runs a dedicated local simulation (Phase 1/2 style)."""
    logger.info("AegisSwarm: Running Local Simulation Mode")
    engine = SimulationEngine()
    try:
        engine.initialize()
    except Exception as e:
        logger.error(f"Failed to initialize simulation engine: {e}")
        return
    engine.start()
    
    try:
        # Keep main thread alive while background engine runs
        import time
        while engine.state.value in ["RUNNING", "PAUSED", "INITIALIZED"]:
            time.sleep(1)
    except KeyboardInterrupt:
        engine.stop()
    finally:
        engine.shutdown()

def run_server():
    """Starts the FastAPI platform server."""
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"AegisSwarm: Starting API Platform on {host}:{port}")
    uvicorn.run("backend.api.server:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AegisSwarm Enterprise AI Platform")
    parser.add_argument("--simulate", action="store_true", help="Run local simulation mode")
    parser.add_argument("--server", action="store_true", help="Start FastAPI backend server")
    
    args = parser.parse_args()
    
    if args.simulate:
        run_local_simulation()
    elif args.server:
        run_server()
    else:
        # Default behavior: run simulation if no args provided, or print help
        run_local_simulation()
