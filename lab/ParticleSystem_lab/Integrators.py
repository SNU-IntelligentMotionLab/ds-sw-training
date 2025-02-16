class Integrator:
    def solve(self, particle_system, time_step):
        pass
    
class Euler(Integrator):
    def solve(self, particle_system, time_step):
        
        particle_system.evaluate_derivative()
        
        for p in particle_system.particles:
            # -------------------------------------
            # TODO (2): Implement Euler Integration
            # -------------------------------------
            a = 0
            p.position += 0 # TODO : Update position
            p.velocity += 0 # TODO : Update velocity

class ImplicitEuler(Integrator):
    def solve(self, particle_system, time_step):
        
        particle_system.evaluate_derivative()
        
        for p in particle_system.particles:
            # -------------------------------------
            # TODO (2): Implement ImplicitEuler Integration
            # -------------------------------------
            a = 0
            p.velocity += 0 # TODO : Update velocity
            p.position += 0 # TODO : Update position

class Midpoint(Integrator):
    def solve(self, particle_system, time_step):
        # -----------------------------
        # TODO (Numerical Method)
        # -----------------------------
        # Save initial position and velocity
        init_position = [p.position.copy() for p in particle_system.particles]
        init_velocity = [p.velocity.copy() for p in particle_system.particles]        
        
        particle_system.evaluate_derivative()
        
        # Compute midpoint position and velocity
        for p in particle_system.particles:
            a = 0           # TODO : Compute acceleration
            p.velocity += 0 # TODO : Compute velocity at midpoint
            p.position += 0 # TODO : Compute position at midpoint
        
        # Compute forces at midpoint
        particle_system.evaluate_derivative()
        
        # Compute final position and velocity
        for i, p in enumerate(particle_system.particles):
            a = 0         # TODO : Compute acceleration
            # p.velocity =  # TODO : Compute final velocity
            # p.position =  # TODO : Compute final position
        
class RK4(Integrator):
    def solve(self, particle_system, time_step):
        # -----------------------------
        # TODO (Numerical Method)
        # -----------------------------
        pass
