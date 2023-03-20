from LBMSimulationInterface import LBMSimulationInterface as LBM_SI
import math

def capillary_number_simulation(Ca, viscosity_ratio, confinement_ratio, system_size):
    """
    Generates a dictionary containing the parameter updates for a simulation with the given capillary number and viscosity ratio.

    Args:
        Ca (float): Capillary number.
        viscosity_ratio (float): Viscosity ratio.

    Returns:
        dict: A dictionary containing parameter updates for the simulation.
    """
    def LBM_viscosity(tau):
        viscosity = (1/3)*(tau - 0.5)
        return viscosity

    # Very low Re
    Re_particle = 0.1
    strain_mod_conversion = 3 # conversion factor between skalak model kappa_s between BioFM and Foessel (2011)

    # Set up the domain size and decomposition
    lattice_NX = system_size; lattice_NY = system_size; lattice_NZ = system_size+2

    # Using Couette flow
    Couette_active = 1

    # Simulation end time
    sim_time_end = 10000000 # must be longer than time to reach steady state

    # Data saving
    particles_VTK_active = 1
    particles_VTK_step = 1000
    particles_statistics_active = 1
    particles_statistics_step = 100

    # Convergence
    steady_active = 1 # activate steady state stopping condition
    steady_threshold = 1e-6 # must ensure small enough
    steady_timeInterval = 1000 # must ensure small enough

    # LBM parameters (using MRT to allow for large tau variations)
    LBM_tau = 1 # the relaxation time
    MRT_active = 1 # using multiple relaxation time model
    MRT_tauBulk = LBM_tau # equal bulk and shear relaxation times
    MRT_Lambda = 1/12

    # Set up particle mesh
    meshRadius = 0.5*(lattice_NZ - 2)*confinement_ratio
    number_of_faces = 20*math.ceil(meshRadius)**2
    meshFile = f"./MeshGenerator/sph_ico_{number_of_faces}.msh"

    # Mesh position
    X = lattice_NX / 2
    Y = lattice_NY / 2
    Z = lattice_NZ / 2

    # Set top and bottom wall velocity based on Re_particle
    velocity = Re_particle * LBM_viscosity(LBM_tau) * (lattice_NZ-2) / (2 * meshRadius**2)
    shear_rate = 2 * velocity / system_size
    Couette_velTopX = velocity 
    Couette_velBotX = -velocity

    # Set particle properties based on Ca and Bq values:
    kS = strain_mod_conversion * LBM_viscosity(LBM_tau)*shear_rate*meshRadius/Ca # set kappa_s by Ca=visc*gammadot*radius/kS
    kalpha = kS # relationship kalpha/ks = 1

    parameter_updates = {
        "parameters.xml": {
            ('lattice', 'size', 'NX'): str(lattice_NX),
            ('lattice', 'size', 'NY'): str(lattice_NY),
            ('lattice', 'size', 'NZ'): str(lattice_NZ),
            ('lattice', 'times', 'end'): str(sim_time_end),
            ('LBM', 'relaxation', 'tau'): str(LBM_tau),
            ('LBM', 'MRT', 'active'): str(MRT_active),
            ('LBM', 'MRT', 'tauBulk'): str(MRT_tauBulk),
            ('LBM', 'MRT', 'Lambda'): str(MRT_Lambda),
            ('data', 'particles', 'VTK','active'): str(particles_VTK_active),
            ('data', 'particles', 'VTK','step'): str(particles_VTK_step),
            ('data', 'particles', 'statistics','active'): str(particles_statistics_active),
            ('data', 'particles', 'statistics','step'): str(particles_statistics_step),
            ('boundaries', 'Couette', 'active'): str(Couette_active),
            ('boundaries', 'Couette', 'velBotX'): str(Couette_velBotX),
            ('boundaries', 'Couette', 'velTopX'): str(Couette_velTopX),
            ('convergence', 'steady', 'active'): str(steady_active),
            ('convergence', 'steady', 'timeInterval'): str(steady_timeInterval),
            ('convergence', 'steady', 'threshold'): str(steady_threshold)
        },
        "parametersMeshes.xml": {
            ('viscosityContrast', 'viscosity', 'ratio'): str(viscosity_ratio),
            ('mesh', 'general', 'file'): meshFile,
            ('mesh', 'general', 'radius'): str(meshRadius),
            ('mesh', 'physics', 'kalpha'): str(kalpha),
            ('mesh', 'physics', 'kS'): str(kS)
        },
        "parametersPositions.xml": {
            ('particle', 'X'): str(X),
            ('particle', 'Y'): str(Y),
            ('particle', 'Z'): str(Z)
        }
    }
    return parameter_updates

def main():
    # Define the path to the template folder containg the meshes, parameteres and executable
    template_folder_path = "./template/"
    
    # set up the interface
    interface = LBM_SI(template_folder_path)

    # parameters which define the problem
    confinement_ratio = 0.2
    system_size = 26
    viscosity_ratio_values = [1,5,10]
    Ca_values = [0.1,0.5,1]

    # run the simulations
    for viscosity_ratio in viscosity_ratio_values:
        for Ca in Ca_values:
            simulation_directory_name = f"./SimFiles/VR_{viscosity_ratio}/Ca_{Ca}/"
            parameter_updates = capillary_number_simulation(Ca, viscosity_ratio, confinement_ratio, system_size)
            interface.run_simulation(simulation_directory_name, parameter_updates)

if __name__ == "__main__":
    main()