import numpy as np
from Constraints import *

class PBDSimulation:
    def __init__(self, 
                 world, 
                 gravity=(0, -9.8, 0), 
                 time_step=0.0333,
                 substeps=2):

        self.world = world
        self.constraints = []
        
        # Physics Parameters
        self.gravity = np.array(gravity, dtype=np.float32)
        self.time_step = time_step
        self.substeps = substeps
        self.h = self.time_step / self.substeps

        # Constraints parameters
        self.collision_compliance = 0.00000001
        self.attach_constraints = []

    def add_constraint(self, constraint):
        if isinstance(constraint, Constraint):
            self.constraints.append(constraint)
        
        if isinstance(constraint, AttachmentConstraint):
            self.attach_constraints.append(constraint)

    def detach_all(self):
        for attach_constraint in self.attach_constraints:
            attach_constraint.anchor = None
    
    def reset(self,):
        for obj in self.world.get_objects():
            obj.curr_pos = obj.init_pos.copy()
            obj.prev_pos = obj.curr_pos.copy()
            obj.vel = np.zeros_like(obj.curr_pos)

        for constraint in self.constraints:
            constraint.reset()
    
    # ==========================================================
    # ================= FILL IN THE CODE BELOW =================
    # ==========================================================
    
    def step(self):
        # TODO (ADVANCED) 
        collisions = self.check_collisions()
        
        for _ in range(self.substeps):
            # --------------------------------------------------
            # TODO (4-1): Generate Contacts
            # --------------------------------------------------
            contacts = None   # TODO: Generate Contacts 

            # --------------------------------------------------
            # TODO (2): Integrate, Solve Constraints(Positions) and Update Velocities
            # - Place self.integrate(), self.solve_positions() and self.update_velocities() in right order
            # --------------------------------------------------
            pass
            
            # --------------------------------------------------
            # TODO (4-2) : Solve Velocities
            # --------------------------------------------------
            pass
            
                    
    def check_collisions(self):
        # TODO (ADVANCED) : Broad Phase Collision Detection for large number of objects.
        return []
    
    def generate_contacts(self, collisions):
        contacts = []
        
        # TODO (ADVANCED) : Dynamic - Dynamic Collisions
        for collision in collisions:
            pass
        
        # --------------------------------------------------
        # TODO (4-1) : Generate Ground Collision Constraints
        # - Find the vertices in contact with the ground
        # - Generate Ground Collision Constraints
        # --------------------------------------------------
        for obj in self.world.get_objects():
            contact_vertices = []              # TODO: Find vertices in contact with the ground
            for id in contact_vertices:
                contacts.append(Constraint())  # TODO: Add Ground Collision Constraint
            
        return contacts
    
    def integrate(self):
        # --------------------------------------------------
        # TODO (2) : Integrate
        # - Update previous position, velocity and current position
        # --------------------------------------------------
        for obj in self.world.get_objects():
            obj.prev_pos = obj.curr_pos.copy()
            obj.vel += 0       # TODO: Fill in velocity update equation
            obj.curr_pos += 0  # TODO: Update position using velocity
            

    def solve_positions(self, contacts=None):        
        for constraint in self.constraints:
            constraint.solve(self.h)
        
        if contacts is None:
            return
        
        for contact in contacts:
            contact.solve(self.h)
            
    def update_velocities(self):
        # --------------------------------------------------
        # TODO (2) : Update Velocities
        # - Update velocities of objects based on the current and previous positions
        # --------------------------------------------------
        for obj in self.world.get_objects():
            continue
            obj.vel = 0       # TODO: Fill in velocity update equation.
              
        
    def solve_velocities(self, contacts):
        for contact in contacts:
            contact.solve_velocity()
            
        
