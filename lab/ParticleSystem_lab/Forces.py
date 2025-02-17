import numpy as np

# Types of forces
# 1. Constant e.g. gravity
# 2. position dependent e.g. forces fields, winds
# 3. velocity dependent e.g. drag, friction
# 4. n-ary e.g. springs
# 5. collision

class Force:
    def apply(self, particles):
        pass

class Gravity(Force):
    def __init__(self, gravity=np.array([0, -9.8])):
        self.G = gravity
        
    def apply(self, particles):
        for p in particles:
            if np.isinf(p.mass):
                continue
            # -----------------------------
            # TODO (3): Implement Gravity
            # -----------------------------
            p.force += 0 # TODO : Implement Gravity
        

class Spring(Force):
    def __init__(self, particle1, particle2,  k_s, k_d, l0):
        self.p1 = particle1
        self.p2 = particle2
        self.k_s = k_s
        self.k_d = k_d
        self.l0 = l0
        
    def apply(self, particles=None):
        # -----------------------------
        # TODO (4) : Implement Spring Force
        # -----------------------------        
        x1 = self.p1.position
        x2 = self.p2.position
        
        l = x1 - x2
        length = np.linalg.norm(l)
        if length < 1e-6:
            return
        
        l_dot = 0  # TODO: Compute l_dot 
        f = 0      # TODO: Compute force
         
        self.p1.force += f
        self.p2.force += -f        
        

class Mouse(Force):
    def __init__(self, particle, target, k_s=100, k_d=1.0):
        self.p = particle
        self.target = target
    
        self.k_s = k_s
        self.k_d = k_d
        
    def apply(self, particles=None):
        # -----------------------------
        # TODO (5) : Implement Mouse Spring
        # -----------------------------
        x = self.p.position
        
        l = self.target - x
        length = np.linalg.norm(l)         
        if length < 1e-6:
            return
         
        l_dot = 0 # TODO : Compute l_dot
        f = 0     # TODO: Compute force
         
        self.p.force += -f


class Drag(Force):
    def __init__(self, k_drag=0.1):
        self.k_drag = k_drag
        
    def apply(self, particles):
        for p in particles:
            # -----------------------
            # TODO (Various Forces): Implement Drag
            # -----------------------
            p.force += 0