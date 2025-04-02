import LBMSimulationInterface as lbmi
import math
import numpy as np
import shutil
import pprint as pp
import os
def cross_slot_simulation(Ca, Z0, X0):
    parameter_updates = lbmi.ParameterUpdates()
    parameter_updates.sim_time(1)
    parameter_updates.checkpoint(-1,-1,-1)

    kS = (1/60)*(0.025*9.6)/(Ca*48)
    kalpha = 2*kS
    kB = 2.87e-3 * kS * 9.6**2
    
    parameter_updates.mesh_kostas(radius=9.6, kV=1, kA=0, kalpha=kalpha, kS=kS,
                               kB=kB, density=1)

    # convert positions to lattice units
    z0 = Z0*(48/2) + (50/2)
    x0 = (560/2) - X0*(80/2)


    parameter_updates.mesh_positions(position=[20, x0, z0], angle="0", axisX="1", axisY="1", axisZ="1")
    return parameter_updates

if __name__ == "__main__":
    Ca_values = [0.001,0.01,0.05]
    Z0_values = [0.49, -0.49, 0, 0.22, -0.22]
    X0_values = [0.0033, 0.01, 0.05, 0.15]

    for Ca in Ca_values:
        for Z0 in Z0_values:
            for X0 in X0_values:
                parameter_updates = cross_slot_simulation(Ca=Ca, Z0=Z0, X0=X0)
                setup = lbmi.SimulationSetup(
                        template_path="kostas_rerun_all/template", 
                        root_path="kostas_rerun_all/data", # the root path for the simulation datas
                        parameter_updates=parameter_updates,
                        overwrite=False, # only set this to true if you're prepared to lose data!
                        simulation_id=f"{Ca}_{Z0}_{X0}"
                    )
                
                setup.run_simulation(num_cores=8, logfile='log.txt')

                # # Remove all Backup folders
                # shutil.rmtree(os.path.join(setup.simulation_directory, "Backup"))
                
                # # # It's good practise to merge the VTK files after the simulation to save space
                # lbmi.merge_all_timesteps(setup.simulation_directory, setup.simulation_directory, num_cores=8)