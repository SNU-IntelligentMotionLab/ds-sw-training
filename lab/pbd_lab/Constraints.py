import numpy as np

class Constraint:
    def __init__(self, compliance=0.0, lambda_=0.0):
        self.compliance = compliance
        self.lambda_ = lambda_
    def solve(self, *args, **kwargs):
        pass
    def solve_velocity(self, *args, **kwargs):
        pass
    def reset(self):
        self.lambda_ = 0.0
        
class DistanceConstraint(Constraint):
    def __init__(self, body1, id1, body2, id2, rest_length, compliance=0.0, lambda_=0.0):
        self.body1 = body1
        self.w1 = self.body1.inv_mass
        self.id1 = id1
        
        self.body2 = body2
        self.w2 = self.body2.inv_mass
        self.id2 = id2
        
        self.rest_length = rest_length
        self.compliance = compliance
        self.lambda_ = lambda_
            
    def solve(self, h):
        # --------------------------------------------------
        # TODO (3) : Distance Constraints
        # --------------------------------------------------
        x1, x2 = self.body1.curr_pos[self.id1], self.body2.curr_pos[self.id2]
        normal = x1 - x2
        length = np.linalg.norm(normal)
        if length < 1e-6:
            return
        
        C = 0    # TODO: C(x1, x2) = ||x1 - x2|| - rest_length
        dC1 = 0  # TODO: dC/dx1 = (x1 - x2) / ||x1 - x2||
        dC2 = 0  # TODO: dC/dx2 = (x2 - x1) / ||x1 - x2||
        if abs(C) < 1e-6:
            return
        
        # Make Constraint Soft!
        alpha = self.compliance / h / h
        dlambda = - (C + alpha * self.lambda_) / (self.w1 + self.w2 + alpha)
        self.lambda_ += dlambda

        dx1 = 0  # TODO: Compute update for x1
        dx2 = 0  # TODO: Compute update for x2
        
        self.body1.curr_pos[self.id1] += dx1
        self.body2.curr_pos[self.id2] += dx2

class GroundCollisionConstraint(Constraint):
    def __init__(self, body, i, compliance=0.0):
        self.body = body
        self.i = i
        self.w = self.body.inv_mass
        
        self.n = np.array([0, 1, 0], dtype=np.float32)
        
        self.compliance = compliance
        
    def solve(self, h):
        # --------------------------------------------------
        # TODO (4-1) : Ground Collision Constraints
        # --------------------------------------------------
        x = self.body.curr_pos[self.i]
        
        C = 0       # TODO: Compute constraint function
        dC = 0      # TODO: Compute constraint gradient
        if C >= 0:  
            return
        
        # Make Constraint Soft!        
        alpha = self.compliance / h / h
        dlambda = -C / (self.w + alpha)  
        
        dx = 0      # TODO: Compute position correction
        
        self.body.curr_pos[self.i] += dx  

    
    def solve_velocity(self):
        # --------------------------------------------------
        # TODO (4-2) : Friction and Restitution
        # --------------------------------------------------
        v = self.body.vel[self.i]
        k_f = self.body.friction
        k_r = self.body.restitution
        
        v_n = 0    # TODO: Compute normal velocity
        v_t = 0    # TODO: Compute tangential velocity
        
        self.body.vel[self.i] = 0  # TODO: Update velocity
          
class AttachmentConstraint(Constraint):
    def __init__(self, body, id, anchor, compliance=0.0, lambda_=0.0):
        self.body = body
        self.id = id
        self.w = self.body.inv_mass
        
        self.init_anchor = np.array(anchor, dtype=np.float32)
        self.anchor = self.init_anchor.copy()
        
        self.compliance = compliance
        self.lambda_ = lambda_       
        
        
    def solve(self, h):
        if self.anchor is None:
            return
        # --------------------------------------------------
        # (2) Attach Constraints
        # - C(x) = ||x - anchor||
        # - dC(x) = (x - anchor) / ||x - anchor||
        # --------------------------------------------------        
        x = self.body.curr_pos[self.id]
        d = x - self.anchor
        length = np.linalg.norm(d)
        
        C = length
        if length < 1e-6:
            return
        dC = d / length
        
        # Make Constraint Soft!
        alpha = self.compliance / h / h
        dlambda = -C / (self.w + alpha)
        dx = dlambda * dC
        
        self.body.curr_pos[self.id] += self.w * dx
        
    
    def reset(self):
        super().reset()
        self.anchor = self.init_anchor.copy()