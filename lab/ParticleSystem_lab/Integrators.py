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
        # Save initial position and velocity
        init_position = [p.position.copy() for p in particle_system.particles]
        init_velocity = [p.velocity.copy() for p in particle_system.particles]
        
        # Step 1: Compute k1
        particle_system.evaluate_derivative()
        k1_v = [p.force / p.mass for p in particle_system.particles]
        k1_x = [p.velocity.copy() for p in particle_system.particles]
        
        # Step 2: Compute k2
        for i, p in enumerate(particle_system.particles):
            pass
            # p.position = # TODO 
            # p.velocity = # TODO
        particle_system.evaluate_derivative()
        k2_v = [p.force / p.mass for p in particle_system.particles]
        k2_x = [p.velocity.copy() for p in particle_system.particles]
        
        # Step 3: Compute k3
        for i, p in enumerate(particle_system.particles):
            pass
            # p.position = # TODO
            # p.velocity = # TODO
        particle_system.evaluate_derivative()
        k3_v = [p.force / p.mass for p in particle_system.particles]
        k3_x = [p.velocity.copy() for p in particle_system.particles]
        
        # Step 4: Compute k4
        for i, p in enumerate(particle_system.particles):
            pass
            # p.position = # TODO 
            # p.velocity = # TODO 
        particle_system.evaluate_derivative()
        k4_v = [p.force / p.mass for p in particle_system.particles]
        k4_x = [p.velocity.copy() for p in particle_system.particles]
        
        # Final update
        for i, p in enumerate(particle_system.particles):
            p.position = init_position[i] + (time_step / 6) * (k1_x[i] + 2 * k2_x[i] + 2 * k3_x[i] + k4_x[i])
            p.velocity = init_velocity[i] + (time_step / 6) * (k1_v[i] + 2 * k2_v[i] + 2 * k3_v[i] + k4_v[i])