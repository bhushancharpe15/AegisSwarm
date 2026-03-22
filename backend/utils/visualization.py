import matplotlib.pyplot as plt
import numpy as np
from typing import Any
from simulation.environment.grid import Environment
from swarm.swarm_manager.manager import SwarmManager

class Visualizer:
    """Handles the visualization of the simulation using Matplotlib."""
    
    def __init__(self, environment: Environment, swarm_manager: SwarmManager):
        self.env = environment
        self.swarm_mgr = swarm_manager
        
        plt.ion() # Interactive mode
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        
    def render(self, step: int):
        """Renders the current state of the simulation."""
        self.ax.clear()
        
        # Draw Terrain
        terrain_grid = self.env.terrain_manager.terrain_grid
        color_grid = np.zeros((*terrain_grid.shape, 3))
        
        for i in range(self.env.width):
            for j in range(self.env.height):
                terrain_type = terrain_grid[i][j]
                color = self.env.terrain_manager.TERRAIN_PROPERTIES[terrain_type]["color"]
                # Convert hex to RGB
                rgb = tuple(int(color.lstrip('#')[i:i+2], 16)/255.0 for i in (0, 2, 4))
                
                # Phase 2: Exploration shading
                if hasattr(self.env, 'explored_mask') and not self.env.explored_mask[i, j]:
                    # Darken unexplored cells
                    rgb = tuple(c * 0.4 for c in rgb)
                    
                color_grid[i, j] = rgb
                
        self.ax.imshow(color_grid.transpose(1, 0, 2), origin='upper')
        
        # Draw Obstacles
        for x, y in self.env.obstacle_manager.static_obstacles:
            self.ax.plot(x, y, 'ks', markersize=10) # Black square
            
        # Draw Events
        for x, y in self.env.events:
            self.ax.plot(x, y, 'y*', markersize=12) # Yellow star
            
        # Draw Robots
        for robot in self.swarm_mgr.robots.values():
            if robot.status == "active":
                self.ax.plot(robot.position[0], robot.position[1], 'ro', markersize=8) # Red circle
                self.ax.text(robot.position[0], robot.position[1] + 0.5, robot.robot_id, 
                            fontsize=8, ha='center', color='white', fontweight='bold')
                
        self.ax.set_title(f"AegisSwarm Simulation - Step {step}")
        self.ax.set_xticks(range(self.env.width))
        self.ax.set_yticks(range(self.env.height))
        self.ax.grid(True, which='both', color='white', linestyle='-', linewidth=0.5, alpha=0.3)
        
        plt.draw()
        plt.pause(0.1)
        
    def close(self):
        plt.ioff()
        plt.show()
