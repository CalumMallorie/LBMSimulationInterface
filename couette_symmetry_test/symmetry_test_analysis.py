import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_taylor_deformation(filepath):
    particle_data = os.path.join(filepath, 'Particles', 'Axes_0.dat')
    particle_df = pd.read_csv(particle_data, sep=' ', comment='#')

    D = (particle_df.a - particle_df.c)/(particle_df.a + particle_df.c)

    return D
    

D_x = calculate_taylor_deformation('couette_symmetry_test/data/x_velocity_merged')
D_y = calculate_taylor_deformation('couette_symmetry_test/data/y_velocity_merged')

plt.plot(D_x, label='x driven flow')
plt.plot(D_y, label='y driven flow')
plt.xlabel('Timestep')
plt.ylabel('Taylor deformation')
plt.legend()
plt.show()