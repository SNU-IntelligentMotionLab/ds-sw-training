import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from Renderer import Renderer2D
from ParticleSystem import ParticleSystem, Particle


vertices = np.array([
    [  0.,   -100.  ],
    [ 22.45,  -30.92],
    [ 95.11,  -30.90],
    [ 36.29,   11.80],
    [ 58.78,   80.90],
    [  0.  ,   38.20],
    [-58.78,   80.90],
    [-36.29,   11.80],
    [-95.11,  -30.90],
    [-22.45,  -30.92]
])

edges = [ (0, 3), (3, 6), (6, 9), (9, 2), (2, 5), (5, 8), (8, 1), (1, 4), (4, 7), (7, 0) ]

def main():
    ps = ParticleSystem()
    ps.ground = None

    # ==================
    # 0. Renderer for Visualization
    # ==================
    ps.renderer = Renderer2D(ps)     
    
    # ==================
    # 1. Create Object
    # ==================
    for i, v in enumerate(vertices):
        ps.add_particle(Particle(v * 1))
    
    for i, j in edges:
        ps.edges.append((i, j))       
    
    # ==================
    # 2. Animation
    # ==================
    def animate(rotation_angle):
        rotation_matrix = np.array([
            [np.cos(rotation_angle), -np.sin(rotation_angle)],
            [np.sin(rotation_angle), np.cos(rotation_angle)]
        ])
        for i in range(len(vertices)):
            ps.particles[i].position = vertices[i] @ rotation_matrix  
    
    # ==================
    # 3. Main Loop
    # ==================        
    angle = 0
    while ps.running:
        pygame.time.wait(10)
        
        # 1. Handle Events (Mouse, Keyboard etc.)
        ps.renderer.handle_events()
        
        # 2. Compute Current State
        if ps.playing:
            animate(angle)
            angle += 0.01
        
        # 3. Render Current State        
        ps.render()
        
        if pygame.event.get(QUIT):
            ps.running = False
    
    pygame.quit()
    
        
    
if __name__ == "__main__":
    main()