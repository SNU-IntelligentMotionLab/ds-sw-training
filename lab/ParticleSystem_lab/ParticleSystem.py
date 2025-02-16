from typing import List, Optional
import numpy as np
from Forces import *
from Integrators import *

class Particle:
    def __init__(self, pos, mass=1.0, radius=5.0):
        self.position = pos
        self.velocity = np.array([0.0, 0.0], dtype=np.float32)
        self.force = np.array([0.0, 0.0], dtype=np.float32)
        self.mass = mass
        
        self.radius = radius
        self.inital_position = pos.copy()
        self.inital_mass = mass
        
        
    def clear_force(self):
        self.force = np.array([0.0, 0.0], dtype=np.float32)

    def reset(self):
        self.position = self.inital_position.copy()
        self.velocity = np.zeros_like(self.position)
        self.clear_force()
    
    def is_attached(self):
        return np.isinf(self.mass)

class ParticleSystem:
    def __init__(self, integrator=None, renderer=None):
            
        # Particle System
        self.particles  : List[Particle]       = []        
        self.forces     : List[Force]          = []
        
        # Differential Equation Solver
        self.integrator : Optional[Integrator] = integrator
        
        # Additional Objects
        self.ground = {
            'normal' : np.array([0.0, 1.0], dtype=np.float32),
            'origin' : np.array([0.0, 0.0], dtype=np.float32),
            'friction' : 0.8,
            'restitution' : 0.3,
        }
        self.edges = []

        
        # Mouse Interaction
        ## Attach
        self.attached_particles = set()
        
        ## Grab
        self.grabbed_particle = None 
        self.grab_force = None
        
        # Rendering
        self.renderer = renderer
        self.running = True
        self.playing = False
        
    def add_particle(self, particle):
        if isinstance(particle, Particle):
            self.particles.append(particle)
    
    def add_force(self, force):
        if isinstance(force, Force):
            self.forces.append(force)

    
    def remove_force(self, force):
        if force in self.forces:
            self.forces.remove(force)
    
    def evaluate_derivative(self,):
        # -----------------------------
        # TODO (2): Implement Derivative Evaluation
        # - Loop over particles, zero force accumulators
        # - Calculate forces by invoking apply functions, sum all forces into accumulators
        # -----------------------------
        for p in self.particles:
            p.clear_force()
        
        for f in self.forces:
            f.apply(self.particles) 
            
        # (3) Contact force
        self.contact_during_ode()         
    
    def step(self, time_step):
        if not self.playing:
            return
        self.integrator.solve(self, time_step)
        self.collision_after_ode()
                        
    def contact_during_ode(self):
        for p in self.particles:
            x, v = p.position, p.velocity   
            n, o = self.ground['normal'], self.ground['origin']
            k_f = self.ground['friction']
        
            penetration_depth = np.dot(x - o, n) - p.radius
            
            # No collision
            if penetration_depth > 1e-3:
                continue
            
            # Resting Contact
            # --------------------------
            # TODO (Collision) : Implement Resting Contact
            # --------------------------
            if np.abs(np.dot(v, n)) < 1e-3:
                if np.dot(n, p.force) < 0:
                    p.force += 0 # TODO : Update "push out" force
                    
                    v_tangent = 0 # TODO : Update tangent velocity
                    p.force += 0 # TODO : Update friction force
        
    def collision_after_ode(self,):
        for p in self.particles:
            x, v = p.position, p.velocity   
            n, o = self.ground['normal'], self.ground['origin']
            k_r = self.ground['restitution']
            
            depth = np.dot(x - o, n) - p.radius
            if depth < 0:
                # --------------------------
                # TODO (Collision) : Implement Collision Response
                # --------------------------
                v_normal = 0    # TODO : Update normal velocity
                v_tangent = 0   # TODO : Update tangent velocity
                
                p.position -= 0 # TODO : Update position
                # p.velocity = 0  # TODO : Update velocity
                
                                    
    def render(self,):
        self.renderer.render()

    # =============================
    # Mouse Interaction
    # =============================
    def attach_particle(self, mouse_pos):
        nearest_particle = self.get_nearest_particle(mouse_pos)
        if nearest_particle:
            # Attach
            if not nearest_particle in self.attached_particles:
                nearest_particle.mass = np.inf
                nearest_particle.velocity = np.zeros_like(nearest_particle.velocity)
                self.attached_particles.add(nearest_particle)
            # Detach
            else:
                nearest_particle.mass = nearest_particle.inital_mass
                self.attached_particles.remove(nearest_particle)
    
    def detach_all_particles(self):
        for p in self.attached_particles:
            p.mass = p.inital_mass
        self.attached_particles.clear()
    
    def start_grab(self, mouse_pos):
        self.grabbed_particle = self.get_nearest_particle(mouse_pos)
        if self.grabbed_particle:
            if self.grabbed_particle in self.attached_particles:
                return
            # -------------------------
            # TODO (5) : Generate Mouse Spring when Mouse is pressed
            # -------------------------
            self.grab_force = None # TODO : Generate Mouse Force object when the mouse is pressed
            
            self.add_force(self.grab_force)

    def update_grab(self, mouse_pos):
        x, y = mouse_pos
        if self.grabbed_particle and self.grab_force:
            self.grab_force.target = np.array([x, y])
    
    def stop_grab(self,):
        if self.grab_force:
            self.remove_force(self.grab_force)
            self.grab_force = None
        self.grabbed_particle = None
    
    def get_nearest_particle(self, mouse_pose):
        x, y = mouse_pose
        min_dist = np.inf
        nearest_particle = None
        for p in self.particles:
            dist = np.linalg.norm(p.position - np.array([x, y]))
            if dist < min_dist and dist < p.radius:
                min_dist = dist
                nearest_particle = p
        return nearest_particle