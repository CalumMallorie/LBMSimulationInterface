from dataclasses import dataclass
from vector import Vector

@dataclass
class Lattice():
    size_x: int
    size_y: int
    size_z: int

    number_of_cores_x: int = 1
    number_of_cores_y: int = 1
    number_of_cores_z: int = 1

    tau: float = 1

    def number_of_cores(self,x,y,z):
        self.number_of_cores_x = x
        self.number_of_cores_y = y
        self.number_of_cores_z = z

@dataclass
class Particle():

    initial_position_x: float
    initial_position_y: float
    initial_position_z: float

    time_IBM_on: int = 0



@dataclass 
class Simulation():
    end_time: int
    info_step: int
    sanity_check_time: int
    checkpoint_save_time: int
    fluid_checkpoint_start_time: int
    particle_checkpoint_start_time: int
    # gravity: 



@dataclass
class Convergence():
    tolerance: float
    begin: int
    step: int
    flag: bool

@dataclass
class DataOut():
    active: bool = 0
    step: int = 0





FluidVTK = DataOut()
FluidVTK.active = True
FluidVTK.step = 100
print(FluidVTK.step)

ParticleVTK = DataOut()
ParticleVTK.active = True
ParticleVTK.step = 100
print(ParticleVTK.step)

Lattice = Lattice(100,100,100)
Lattice.tau = 0.55
print(Lattice.tau)

    # def __init__(self):
    #     # number of cores in x, y, z directions
    #     self.nx = nx; self.ny = ny; self.nz = nz

    #     # system size
    #     self.Lx = Lx; self.Ly = 100; self.Lz = 100
        
        # # simulation and checkpoint times
        # self.t_end = args.t_end; self.t_info = 1000; self.t_sanity = 100000
        # self.checkpoint_saveStep = 100000; self.checkpoint_timeLBM = -1; self.checkpoint_timeMEM = -1#

        # # IBM time
        # self.timeIBMon = args.timeIBMon
        
        # # relaxation time
        # self.tau = args.tau
        
        # # fluid forcing
        # self.force_x = 0; self.force_y = 0; self.force_z = 0
        
        # # saving fluid data
        # self.fluidVTK_flag = 1; self.fluidVTK_step = args.fluidVTK_step
        # self.fluidStats_flag = 1; self.fluidStats_step = 100
        
        # # saving particle data
        # self.particleVTK_flag = 1; self.particleVTK_step = args.particleVTK_step
        # self.particleStats_flag = 1; self.particleStats_step = 100
        
        # # convergence parameters
        # if args.convergence_tolerance is not None:
        #     self.convergence_flag = 1
        # else:
        #     self.convergence_flag = 0

        # self.convergence_tolerance = args.convergence_tolerance
        # self.convergence_step = 100; self.convergence_t_ignore = args.convergence_t_ignore

# class Mesh():
#     '''
#     A class to store all the parameters relating to the particle mesh.
    
#     The class is initialised using default values, which will be entered into the
#     parameter files unless otherwise specified.
#     '''
#     def __init__(self,args):
#         # membrane size
#         self.radius = 10; self.numFaces = 2000
        
#         # membrane location
#         self.X = 50; self.Y = 50; self.Z = 50
        
#         # membrane physics parameters
#         self.kV = 0.75; self.kA = 0
#         self.kalpha = 0; self.kS = 0; self.kB = 0
#         self.shearViscosity = 0; self.dilationalViscosity = 0; self.kMaxwell_shear = args.k_s; self.kMaxwell_dilation = args.k_d
