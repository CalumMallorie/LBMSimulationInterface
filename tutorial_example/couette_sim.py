import LBMSimulationInterface as lbmi
import math

def couette_sim(Re_p, Ca, confinement, length_z):
    """
    This function computes the necessary XML parameter changes from the given
    physical parameters. Parameters that remain constant across simulations
    should be set in the template files. Customize this function to generate
    parameter files for different individual simulations within a campaign.
    """

    # Initialise the parameter updates class
    parameter_updates = lbmi.ParameterUpdates()

    # Set up the domain size
    parameter_updates.lattice(NX=length_z,NY=length_z,NZ=length_z)

    # Set the domain decomposition
    parameter_updates.MPI(mpi=(2,2,1))

    # Set the relaxation time to 1
    tau = 1
    parameter_updates.relaxation(tau=tau)

    # Set up particle mesh and get the mesh name
    meshRadius = 0.5*(length_z - 2)*confinement
    number_of_faces = 20*math.ceil(meshRadius)**2
    meshFile = f"./MeshGenerator/sph_ico_{number_of_faces}.msh"

    # Mesh centroid position
    X = length_z / 2
    Y = length_z / 2
    Z = length_z / 2

    # Set top and bottom wall velocity based on Re_particle
    tau=1
    velocity = Re_p * lbmi.calculate_viscosity(tau) * (length_z-2) / (2 * meshRadius**2)
    shear_rate = 2 * velocity / length_z
    Couette_velTopX = velocity 
    Couette_velBotX = -velocity
    parameter_updates.couette(vel_bot_x=Couette_velBotX, vel_bot_y=0, vel_top_x=Couette_velTopX, vel_top_y=0) # the y velocities are zero

    # Set particle properties based on Ca and Bq values:
    kS = lbmi.calculate_viscosity(tau)*shear_rate*meshRadius/Ca # set kappa_s by Ca=visc*gammadot*radius/kS
    kalpha = kS # relationship kalpha/ks = 1

    # Update the parameter_updates class with the mesh properties
    parameter_updates.mesh(
        radius=meshRadius,
        kV=0, 
        kA=1, 
        kalpha=kalpha, 
        kS=kS, 
        kB=0
    )

    return parameter_updates

if __name__ == '__main__':
    # We are going to loop over three values of capillar number, and keep
    # Reynolds number and confinement constant:
    Re_p = 1
    confinement = 0.5

    for Ca in [0.01, 0.1, 1]:

        # Get the parameter updates
        parameter_updates = couette_sim(Re_p, Ca, confinement, length_z=32)

        setup = lbmi.SimulationSetup(
            template_path="tutorial_example/template", 
            root_path="tutorial_example/data", # the root path for the simulation datas
            parameter_updates=parameter_updates,
            simulation_id=f'Ca={Ca}', # the subfolder name (counts from 0 if not specified)
            overwrite=True, # only set this to true if you're prepared to lose data!
        )
        setup.run_simulation(num_cores=4)

        # It's good practise to merge the VTK files after the simulation to save space
        lbmi.merge_latest_fluid_vtk_files(setup.simulation_directory+"/VTKFluid/")