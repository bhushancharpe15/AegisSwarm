import time
import numpy as np
import threading
from enum import Enum
from typing import List, Tuple, Dict, Any, Optional
fromsimulation.environment.grid import Environment
fromswarm.swarm_manager.manager import SwarmManager
fromutils.visualization import Visualizer
frommonitoring.logging.logger import logger
frommonitoring.metrics.tracker import metrics
fromconfig.settings import settings

class MissionState(Enum):
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"

class SimulationEngine:
    """Enterprise-grade simulation engine with state management and external control."""
    
    def __init__(self):
        self.env = Environment(settings.GRID_SIZE[0], settings.GRID_SIZE[1])
        self.swarm_mgr = SwarmManager()
        self.viz = None
        self.state = MissionState.INITIALIZED
        self.step_count = 0
        self._no_progress_steps = 0
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _build_fresh_world(self):
        self.env = Environment(settings.GRID_SIZE[0], settings.GRID_SIZE[1])
        self.swarm_mgr = SwarmManager()
        self.viz = None

    def _sync_metrics(self):
        metrics.robots_active = len([r for r in self.swarm_mgr.robots.values() if r.status == "active"])
        metrics.cells_explored = int(np.sum(self.env.explored_mask))

    def get_coverage_percent(self) -> float:
        return float(np.sum(self.env.explored_mask) / (self.env.width * self.env.height) * 100)

    def get_runtime_state(self) -> Dict[str, Any]:
        return {
            "step": self.step_count,
            "status": self.state.value,
            "robots": [
                {
                    "id": r.robot_id,
                    "x": r.position[0],
                    "y": r.position[1],
                    "energy": r.energy_level,
                    "status": r.status,
                }
                for r in self.swarm_mgr.robots.values()
            ],
            "metrics": {
                "coverage_percent": self.get_coverage_percent(),
                "active_robots": len([r for r in self.swarm_mgr.robots.values() if r.status == "active"]),
                "collisions": metrics.collisions_detected,
                "events_detected": len(self.swarm_mgr.comm_hub.get_shared_knowledge().get("events", [])),
            },
            "heatmap": self.env.heatmap_grid.tolist(),
        }
        
    def initialize(self):
        """Standard initialization."""
        logger.info("Initializing Simulation Engine...")
        self._build_fresh_world()
        metrics.reset()
        self.env.generate_grid(settings.OBSTACLE_DENSITY, settings.EVENT_DENSITY)
        self.swarm_mgr.initialize_swarm(
            num_robots=settings.NUM_ROBOTS,
            grid_size=settings.GRID_SIZE,
            sensor_range=settings.SENSOR_RANGE,
            energy_level=settings.INITIAL_ENERGY,
            environment=self.env,
        )
        for robot in self.swarm_mgr.robots.values():
            self.env.mark_explored(robot.position[0], robot.position[1], settings.COVERAGE_MARK_RADIUS)

        self.step_count = 0
        self._no_progress_steps = 0
        self._sync_metrics()
            
        if settings.SHOW_VISUALIZATION:
            self.viz = Visualizer(self.env, self.swarm_mgr)
            
        self.state = MissionState.INITIALIZED
        logger.info("Simulation Engine initialized.")

    def start(self):
        """Starts the simulation in a background thread."""
        if self.state in [MissionState.RUNNING, MissionState.PAUSED]:
            logger.warning("Simulation already running or paused.")
            return

        if self.state == MissionState.COMPLETED:
            logger.info("Simulation completed; resetting before restart.")
            self.reset()

        self._stop_event.clear()
        self._pause_event.clear()
        self.state = MissionState.RUNNING
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("Simulation mission started.")

    def pause(self):
        """Pauses the simulation execution."""
        if self.state == MissionState.RUNNING:
            self._pause_event.set()
            self.state = MissionState.PAUSED
            logger.info("Simulation mission paused.")

    def resume(self):
        """Resumes a paused simulation."""
        if self.state == MissionState.PAUSED:
            self._pause_event.clear()
            self.state = MissionState.RUNNING
            logger.info("Simulation mission resumed.")

    def stop(self):
        """Stops the simulation mission."""
        self._stop_event.set()
        self._pause_event.clear()
        self.state = MissionState.STOPPED
        logger.info("Simulation mission stopped.")

    def reset(self):
        """Resets the simulation to initial state."""
        self.stop()
        if self._thread:
            self._thread.join(timeout=2.0)
        self._thread = None
        self.initialize()
        logger.info("Simulation mission reset.")

    def _run_loop(self):
        """Main execution loop running in a background thread."""
        try:
            while not self._stop_event.is_set() and self.step_count < settings.MAX_STEPS:
                # Handle pause
                while self._pause_event.is_set() and not self._stop_event.is_set():
                    time.sleep(0.1)
                
                if self._stop_event.is_set():
                    break

                self.step_count += 1
                metrics.simulation_steps = self.step_count
                previous_explored = metrics.cells_explored
                
                # logic
                self.env.update_environment()
                robot_positions = [r.position for r in self.swarm_mgr.robots.values()]
                
                for robot_id, robot in self.swarm_mgr.robots.items():
                    if robot.status != "active": continue
                    robot.scan_environment(self.env)
                    other_positions = [pos for pos in robot_positions if pos != robot.position]
                    best_action_pos = robot.decision_engine.choose_best_action(
                        robot_id=robot_id, current_pos=robot.position,
                        environment=self.env, other_robots_pos=other_positions,
                        path_history=robot.path_history,
                        sensor_range=robot.sensor_range,
                    )
                    if self.env.is_valid_position(*best_action_pos) and best_action_pos not in other_positions:
                        robot.move(best_action_pos)
                    self.env.mark_explored(robot.position[0], robot.position[1], settings.COVERAGE_MARK_RADIUS)
                    
                # Update metrics
                self._sync_metrics()

                if metrics.cells_explored > previous_explored:
                    self._no_progress_steps = 0
                else:
                    self._no_progress_steps += 1
                
                if self.viz:
                    self.viz.render(self.step_count)
                    
                if metrics.robots_active == 0:
                    self.state = MissionState.COMPLETED
                    break

                if self.get_coverage_percent() >= settings.TARGET_COVERAGE_PERCENT:
                    self.state = MissionState.COMPLETED
                    logger.info(
                        f"Coverage target reached: {self.get_coverage_percent():.2f}% / {settings.TARGET_COVERAGE_PERCENT:.2f}%"
                    )
                    break

                if self._no_progress_steps >= settings.NO_PROGRESS_STEP_LIMIT:
                    self.state = MissionState.COMPLETED
                    logger.info(
                        f"Mission completed due to no new coverage for {self._no_progress_steps} consecutive steps. Final coverage: {self.get_coverage_percent():.2f}%"
                    )
                    break
                    
                time.sleep(settings.SIMULATION_SPEED)
                
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
        finally:
            self.state = MissionState.COMPLETED if self.step_count >= settings.MAX_STEPS else self.state
            logger.info(f"Loop finished. Final state: {self.state}")

    def shutdown(self):
        self.stop()
        if self.viz:
            self.viz.close()
