from Simulation import PBDSimulation  
from Renderer import Renderer
from Controls import OrbitCamera  
from Objects import Cube, Plane
from Constraints import *

def initWorld(world):
    # ===========================
    # Simulation, Renderer
    # ===========================
    
    world.simulation = PBDSimulation(
        world=world,
        gravity=(0, -9.8, 0),
        time_step=1/60,
        substeps=10
        
    )
    
    world.renderer = Renderer(
        world=world,
        camera=OrbitCamera(
            distance=27.0, 
            theta=51.0, 
            phi=73.0, 
        )
    )
    
    # =============================
    # Create Objects
    # =============================    
    
    # ---------------------------------
    # TODO (1): Set Ground
    # ---------------------------------
    ground = Plane(size=100, color=(0.5, 0.5, 0.5, 0.9))
    world.set_ground(ground)

    # ---------------------------------
    # TODO (1): Draw Cube
    # ---------------------------------
    #    3-------2
    #   /|      /|
    #  7-------6 |      <- Back face (0,1,2,3)
    #  | |     | |      
    #  | 0-----|-1      <- Front face (4,5,6,7)
    #  |/      |/
    #  4-------5       
    # ---------------------------------
    cube1 = None # TODO: Create Cube
    # cube1 = Cube(width=1.0, height=2.0, depth=1.0, positions=[0, 4.5, 0], rotation=[0, 0, 0], color=(1.0, 0.0, 0.0, 1.0))
    world.add_object(cube1)
    

    # =============================
    # Generate Constraints
    # =============================
    
    attach_comp = 0.00001
    rigid_comp = 0.00000001
    hinge_comp = 0.000000
    world.simulation.collision_compliance = 0.00000001

    # ---------------------------------
    # a. Attach Constraint
    # TODO (2) : Add Attach Constraints
    # ---------------------------------
    # world.simulation.add_constraint(AttachmentConstraint(cube1, 2, cube1.curr_pos[2], compliance=attach_comp))


    # ---------------------------------
    # b. Rigid Constraint
    # TODO (3) : Add Rigid Constraints
    # ---------------------------------
    for cube in world.get_objects():
        if cube is not None:
            for edge in cube.edges:
                rest_length = 0                                # TODO: Compute rest length
                world.simulation.add_constraint(Constraint())  # TODO: Add Distance Constraint
    
    # ---------------------------------
    # c. Hinge Constraint
    # TODO (5) : Connect Objects
    # ---------------------------------
    # world.simulation.add_constraint(DistanceConstraint(cube1, 5, cube2, 6, rest_length=0.0, compliance=hinge_comp))
    # world.simulation.add_constraint(DistanceConstraint(cube1, 1, cube2, 2, rest_length=0.0, compliance=hinge_comp))
    

    return world




class World:
    def __init__(self,):
        # Objects
        self.objects = []
        self.ground = None
        
        # Simulation
        self.simulation = None
        self.sim_time = 0.0
        self.playing = False

        # Rendering
        self.renderer = None
        self.running = True
    
    def set_ground(self, ground):
        self.ground = ground    

    def add_object(self, obj):
        if obj is not None:
            self.objects.append(obj)
    
    def get_objects(self):
        return self.objects    
    
    def reset(self):
        self.simulation.reset()
        self.sim_time = 0.0
    
    def step(self):
        if self.playing:
            self.simulation.step()
            self.sim_time += self.simulation.time_step

    def render(self, ):
        self.renderer.render()

    def handle_events(self):
        self.renderer.handle_events()
