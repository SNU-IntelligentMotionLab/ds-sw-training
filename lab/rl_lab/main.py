import pygame
from pygame.locals import *
import time

# from OpenGL.GL import *
# from OpenGL.GLU import *

from World import World, initWorld

def main():
    # ===========================
    # Init World
    # ===========================
    world = initWorld(World())
       
    # ============================
    # Main Loop
    # ============================
    SIM_TIME_STEP = world.simulation.time_step  

    # Time tracking
    accumulated_time = 0.0
    last_sim_time = time.time()

    while world.running:     
        world.handle_events()
                
        # Simulation time step
        now = time.time()
        elapsed = now - last_sim_time
        last_sim_time = now
        accumulated_time += elapsed
        while accumulated_time >= SIM_TIME_STEP:
            world.step()  
            accumulated_time -= SIM_TIME_STEP 
        
        world.render()
        

    pygame.quit()
        
    
if __name__ == "__main__":
    main()