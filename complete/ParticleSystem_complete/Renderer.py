import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class Renderer2D:
    def __init__(self, ps, width=800, height=600):
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("2D Simulation")
        
        # OpenGL Setup
        glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
        glDisable(GL_DEPTH_TEST)          # No depth testing in 2D
        
        # Set Up 2D Projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-width // 2, width // 2, -height // 2, height // 2, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
        # UI Panel Setup
        self.font = pygame.font.Font(None, 24)
        
        # Particle System to Render
        self.ps = ps        
    
    def handle_events(self):
        mouse_pos = self.get_mouse_world_pos()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.ps.playing = not self.ps.playing
                    
                if event.key == K_ESCAPE:
                    self.ps.running = False
                    
                if event.key == K_r:
                    for p in self.ps.particles:
                        p.reset()
                    self.ps.playing = False
                    
                if event.key == K_d and pygame.key.get_mods() & KMOD_CTRL:
                    self.ps.detach_all_particles()
            
            # Mouse Events
            elif event.type == MOUSEBUTTONDOWN:
                    keys = pygame.key.get_pressed()
                    
                    if event.button ==1 and keys[K_LCTRL]:
                        self.ps.attach_particle(mouse_pos)
                    
                    elif event.button == 1:
                        self.ps.start_grab(mouse_pos)

            elif event.type == MOUSEMOTION:
                self.ps.update_grab(mouse_pos)

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.ps.stop_grab()
            
            elif event.type == QUIT:
                self.ps.running = False

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        for (i, j) in self.ps.edges:
            self.draw_edge(self.ps.particles[i], self.ps.particles[j])
        
        for particle in self.ps.particles:
            self.draw_particle(particle)                

        # Draw Ground
        self.draw_ground()
        
        # Draw Mouse Spring
        self.draw_mouse_spring()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_particle(self, particle):
        
        # Color Red if attached
        if particle.is_attached():
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(0.0, 0.0, 0.0)
               
        # Draw Circle
        num_segments = 16
        theta = 2 * np.pi / 16
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*particle.position) 
        for i in range(num_segments + 1):
            angle = theta * i
            x = particle.position[0] + np.cos(angle) * particle.radius
            y = particle.position[1] + np.sin(angle) * particle.radius
            glVertex2f(x, y)
        glEnd()
        
    def draw_edge(self, particle1, particle2):
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(*particle1.position)
        glVertex2f(*particle2.position)
        glEnd()
    
    def draw_ground(self):
        if not self.ps.ground:
            return
        
        # Compute Line Segment
        n, o = self.ps.ground['normal'], self.ps.ground['origin']
        max_length = max(self.screen.get_width(), self.screen.get_height())
        v1 = o + max_length * np.array([-n[1], n[0]])
        v2 = o - max_length * np.array([-n[1], n[0]])
        
        # Draw Line
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)
        glVertex2f(*v1)
        glVertex2f(*v2)
        glEnd()
    
    def draw_mouse_spring(self):
        if self.ps.grabbed_particle and self.ps.grab_force:
            glColor3f(0.0, 1.0, 0.0)
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex2f(*self.ps.grabbed_particle.position)
            glVertex2f(*self.ps.grab_force.target)
            glEnd()
        # Reset line width
        glLineWidth(1)
        
    def get_mouse_world_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Flip Y-axis since Pygame has (0,0) at the top-left
        mouse_y = self.screen.get_height() - mouse_y  

        near_x, near_y, _ = gluUnProject(
            float(mouse_x), 
            float(mouse_y), 
            0.0, 
            glGetDoublev(GL_MODELVIEW_MATRIX), 
            glGetDoublev(GL_PROJECTION_MATRIX), 
            glGetIntegerv(GL_VIEWPORT)
        )
        return np.array([near_x, near_y])

    def draw_ui(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.screen.get_width(), 0, self.screen.get_height(), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        keymap_texts = [
            "Controls:",
            "[Left Mouse] Drag Particle",
            "[Ctrl + Left Mouse] Attach/Detach Particle",
            "[Ctrl + D] Detach All Particles",
            "---------------------------------------------------",
            "[SPACE] Start / Stop Simulation",
            "[R] Reset Simulation",
            "[ESC] Quit"
        ]

        y_offset = 20
        for text in keymap_texts:
            self.render_text(text, 20, self.screen.get_height() - y_offset)
            y_offset += 25
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def render_text(self, text, x, y):
        """ Renders text at a given (x, y) position using OpenGL texture mapping """
        font_surface = self.font.render(text, True, (0, 0, 0))  # Black text
        text_data = pygame.image.tostring(font_surface, "RGBA", True)
        text_width, text_height = font_surface.get_size()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        glPushAttrib(GL_CURRENT_BIT)
        glColor3f(1.0, 1.0, 1.0)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(x, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + text_width, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + text_width, y - text_height)
        glTexCoord2f(0, 0)
        glVertex2f(x, y - text_height)
        glEnd()
        
        glPopAttrib()
        

        glDeleteTextures([texture])
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
