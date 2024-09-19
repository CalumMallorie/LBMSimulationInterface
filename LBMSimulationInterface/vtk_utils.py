# vtk_utils.py

import glob
import re
import numpy as np
import pyvista as pv
import os

def merge_latest_fluid_vtk_files(data_path: str) -> pv.RectilinearGrid:
    """
    Merge VTK files from different cores into a single rectilinear grid.

    Args:
        data_path (str): Path to the directory containing VTK files.

    Returns:
        pyvista.RectilinearGrid: Interpolated rectilinear grid of the merged data.
    """
    print('Finding the largest timestep and merging the VTK files...')
    # Find all VTK files matching the pattern
    file_pattern = f"{data_path}Fluid_p*_t*.vtk"
    file_list = glob.glob(file_pattern)

    if not file_list:
        raise FileNotFoundError("No VTK files found matching the pattern.")

    # Extract timesteps and find the largest timestep
    timesteps = [
        int(re.search(r"_t(\d+).vtk", f_name).group(1)) for f_name in file_list
    ]
    largest_timestep = max(timesteps)

    # Update the file pattern with the largest timestep
    file_pattern = f"{data_path}Fluid_p*_t{largest_timestep}.vtk"
    file_list = glob.glob(file_pattern)

    if not file_list:
        raise FileNotFoundError(f"No VTK files found for timestep {largest_timestep}.")

    # Sort the file list by core number
    file_list.sort(key=lambda x: int(re.search(r"_p(\d+)_", x).group(1)))

    # Read and collect mesh objects
    meshes = [pv.read(f_name) for f_name in file_list]

    # Merge mesh objects
    merged = meshes[0].merge(meshes[1:])

    # Create a rectilinear grid
    x_min, x_max, y_min, y_max, z_min, z_max = merged.bounds
    x_lin = np.arange(x_min, x_max + 1, 1)
    y_lin = np.arange(y_min, y_max + 1, 1)
    z_lin = np.arange(z_min, z_max + 1, 1)
    grid = pv.RectilinearGrid(x_lin, y_lin, z_lin)

    # Interpolate the merged mesh onto the rectilinear grid
    result = grid.interpolate(merged)

    result.save(os.path.join(data_path,"merged.vtr"))
    print(f'Merged VTK files saved as {os.path.join(data_path,"merged.vtr")}')
