from LBMSimulationInterface import LBMSimulationInterface as LBM_SI
import math
import pandas as pd
import matplotlib.pyplot as plt

def capillary_number_simulation(Ca, Re_particle, confinement_ratio, length_z, tau, shear_time):

    

    # Set up the domain size and decomposition
    lattice_NX = length_z; lattice_NY = length_z; lattice_NZ = length_z+2

    # Set up particle mesh
    meshRadius = 0.5*(lattice_NZ - 2)*confinement_ratio
    number_of_faces = 20*math.ceil(meshRadius)**2
    meshFile = f"./MeshGenerator/sph_ico_{number_of_faces}.msh"

    # Mesh position
    X = lattice_NX / 2
    Y = lattice_NY / 2
    Z = lattice_NZ / 2

    # Set top and bottom wall velocity based on Re_particle
    velocity = Re_particle * LBM_viscosity(tau) * (lattice_NZ-2) / (2 * meshRadius**2)
    shear_rate = 2 * velocity / length_z
    Couette_velTopX = velocity 
    Couette_velBotX = -velocity

    # Set the number of timesteps by shear rate:
    num_timesteps = shear_time / shear_rate

    # Set particle properties based on Ca and Bq values:
    kS = LBM_viscosity(tau)*shear_rate*meshRadius/Ca # set kappa_s by Ca=visc*gammadot*radius/kS
    kalpha = kS # relationship kalpha/ks = 1


    # parameter file updates are stored in a dictionary of key-value pairs,
    #   where the key is a tuple specifying the xml path to the parameter
    parameter_updates = {
        "parameters.xml": {
            ('lattice', 'size', 'NX'): str(lattice_NX),
            ('lattice', 'size', 'NY'): str(lattice_NY),
            ('lattice', 'size', 'NZ'): str(lattice_NZ),
            ('lattice', 'times', 'end'): str(num_timesteps),
            ('LBM', 'relaxation', 'tau'): str(tau),
            ('boundaries', 'Couette', 'velBotX'): str(Couette_velBotX),
            ('boundaries', 'Couette', 'velTopX'): str(Couette_velTopX),
        },
        "parametersMeshes.xml": {
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

def calc_shear_rate(Re_particle, confinement_ratio, length_z, tau):
    lattice_NZ = length_z+2
    meshRadius = 0.5*(lattice_NZ - 2)*confinement_ratio
    velocity = Re_particle * LBM_viscosity(tau) * (lattice_NZ-2) / (2 * meshRadius**2)
    shear_rate = 2 * velocity / length_z
    return shear_rate

def LBM_viscosity(tau):
        viscosity = (1/3)*(tau - 0.5)
        return viscosity

def plot_simulation(Ca, simulation_directory_name, Re_particle, confinement_ratio, length_z, tau):
    data_path = simulation_directory_name + "Particles/Axes_0.dat"
    data = pd.read_csv(data_path, sep=' ',skiprows=6)
    data['Taylor_deformation'] = (data['a']-data['c'])/(data['a']+data['c'])
    shear_rate = calc_shear_rate(Re_particle, confinement_ratio, length_z, tau)
    plt.plot(shear_rate*data['time'],data['Taylor_deformation']/Ca)

def main():
    # define the path to the template folder containg the meshes, parameteres and executable
    template_folder_path = "./template/"
    
    # set up the interface
    sim = LBM_SI(template_folder_path)

    # parameters which define the problem
    confinement_ratio = 0.5
    Re_particle = 1
    Ca = 0.01
    tau_range = [0,1,1.1]
    shear_time = 1
    length_z = 48

    # run the simulation in a folder named after the parameters
    for tau in tau_range:
        simulation_directory_name = f"./SimFiles/tau{tau}/"
        parameter_updates = capillary_number_simulation(Ca, Re_particle, confinement_ratio, length_z, tau, shear_time)
        sim.run_simulation(simulation_directory_name, parameter_updates,num_cores=2)
        plot_simulation(Ca,simulation_directory_name, Re_particle, confinement_ratio, length_z, tau)
    plt.show()



if __name__ == "__main__":
    main()