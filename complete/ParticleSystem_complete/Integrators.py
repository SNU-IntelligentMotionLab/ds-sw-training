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
            a = p.force / p.mass
            p.position += p.velocity * time_step
            p.velocity += a * time_step

class ImplicitEuler(Integrator):
    def solve(self, particle_system, time_step):
        
        particle_system.evaluate_derivative()
        
        for p in particle_system.particles:
            # -------------------------------------
            # TODO (2): Implement ImplicitEuler Integration
            # -------------------------------------
            a = p.force / p.mass
            p.velocity += a * time_step
            p.position += p.velocity * time_step

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
            a = p.force / p.mass
            p.velocity = p.velocity + a * time_step / 2
            p.position = p.position + p.velocity * time_step / 2
        
        # Compute forces at midpoint
        particle_system.evaluate_derivative()
        
        # Compute final position and velocity
        for i, p in enumerate(particle_system.particles):
            a = p.force / p.mass
            p.velocity = init_velocity[i] + a * time_step
            p.position = init_position[i] + p.velocity * time_step
        
class RK4(Integrator):
    def solve(self, particle_system, time_step):
        # -----------------------------
        # TODO (Numerical Method)
        # -----------------------------
        pass
