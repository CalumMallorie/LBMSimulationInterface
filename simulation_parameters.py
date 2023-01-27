from vector import Vector3D


class Lattice():
    def __init__(self,size_x,size_y,size_z):
        # System size
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z

        # Number of cores domain is split into
        self.cores = Vector3D(1,1,1)

        # Relaxation time
        self.tau = None

    def parallelise(self,x,y,z):
        '''Sets the number of parallel cores domain is split into'''
        self.cores = Vector3D(x,y,z)
    
    def viscosity(self):
        '''Calculates the lattice viscosity based on tau'''
        viscosity = (1/3)*(self.tau - 0.5)
        return viscosity

    def set_cross_slot(self,CrossSlot):
        

class Particle():
    def __init__(self,x,y,z):
        self.initial_position = Vector3D(x,y,z)
        self.time_IBM_on = 0
        self.radus = 0
        self.kV = 0.75
        self.kA = 0
        self.kalpha = 0
        self.kS = 0
        self.kB = 0
        self.shearViscosity = 0
        self.dilationalViscosity = 0
        self.kMaxwell_shear = 0
        self.kMaxwell_dilation = 0

class Convergence():
    def __init__(self):
        self.tolerance = None
        self.begin = None 
        self.step = None
        self.flag = 0

class Checkpointing():
    def __init__(self):
        self.save_time = None
        self.fluid_start_time = -1
        self.particle_start_time = -1

class Simulation():
    def __init__(self,end_time):
        self.end_time = end_time
        self.info_step = 100
        self.sanity_check_time = 10000
        self.convergence = Convergence()
        self.gravity = Vector3D(0,0,0)
        self.checkpoint = Checkpointing()

class DataOut():
    def __init__(self):
        self.active = 0
        self.step = 0
