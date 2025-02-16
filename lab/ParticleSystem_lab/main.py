import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from Forces import *
from Integrators import *
from Renderer import Renderer2D
from ParticleSystem import ParticleSystem, Particle

   

def main():
    # ===========================
    # 0. Particle System, Integrator, Renderer
    # ===========================
    ps = ParticleSystem()
    ps.integrator = Midpoint()
    ps.renderer = Renderer2D(ps)
     
    # =============================
    # 1. Create Objects
    # =============================  
    ps.ground.update({
        'normal' : np.array([0.0, 1.0], dtype=np.float32),
        'origin' : np.array([0.0, -100.0], dtype=np.float32),
    })
    
    # -----------------------------
    # TODO (1) : Draw Particles
    # - (ADVANCED) Try more complex mesh!
    # -----------------------------
    width, height = 5, 5
    spacing = 25.0  
    for i in range(width):
        for j in range(height):
            x = i * spacing
            y = j * spacing
            ps.add_particle(Particle(np.array([x, y], dtype=np.float32)))
    
    # -----------------------------
    # TODO (4) : Add edges for constraints
    # - (ADVANCED) Consider adding more edges!
    # -----------------------------
    for i in range(width):
        for j in range(height):
            if i < width - 1:
                ps.edges.append((i * height + j, (i + 1) * height + j))
            if j < height - 1:
                ps.edges.append((i * height + j, i * height + j + 1))
    
    # =============================
    # 2. Add Forces
    # =============================
    
    # -----------------------------
    # a. Gravity - Constant
    # TODO (3) : Add Gravity Force
    # -----------------------------    
    ps.add_force(Gravity(gravity=np.array([0, -9.8])))
    
    
    # -----------------------------
    # b. Spring - n-ary
    # TODO (4): Add Spring Force
    # -----------------------------    
    k_s = 100
    k_d = 2
    for i, j in ps.edges:
        # ps.add_force(Force()) # TODO : Add Spring Force
        
        ps.add_force(Spring(ps.particles[i], ps.particles[j], k_s, k_d, spacing))
    
    
    # -----------------------------
    # c. Drag - Velocity Dependent
    # TODO (Additional Forces): Add Drag Force
    # -----------------------------
    # ps.add_force(Drag(k_drag=0.1))
    
    
    
        
    # ============================
    # 3. Main Loop
    # ============================
    while ps.running:
        pygame.time.wait(10)
        
        ps.renderer.handle_events()
        ps.step(1/30)
        ps.render()
        
        
    
if __name__ == "__main__":
    main()