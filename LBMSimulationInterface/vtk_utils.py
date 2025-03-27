# vtk_utils.py

import glob
import re
import numpy as np
import pyvista as pv
import os
import pathlib
import itertools as it
import shutil
from typing import List, Union
import joblib as jb
import tqdm as tm

def merge_latest_fluid_vtk_files(data_path: str) -> pv.RectilinearGrid:
    """
    Merge VTK files from different cores for the largest timestep into a single rectilinear grid.

    Args:
        data_path (str): Path to the directory containing VTK files.

    Returns:
        pyvista.RectilinearGrid: Interpolated rectilinear grid of the merged data.
    """
    print('Finding the largest timestep and merging the VTK files...')
    # Find all VTK files matching the pattern
    file_pattern = os.path.join(data_path, "Fluid_p*_t*.vtk")
    file_list = glob.glob(file_pattern)

    if not file_list:
        raise FileNotFoundError("No VTK files found matching the pattern.")

    # Extract timesteps and find the largest timestep
    timesteps = [
        int(re.search(r"_t(\d+).vtk", f_name).group(1)) for f_name in file_list
    ]
    largest_timestep = max(timesteps)

    # Update the file pattern with the largest timestep
    file_pattern = os.path.join(data_path, f"Fluid_p*_t{largest_timestep}.vtk")
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

    output_file = os.path.join(data_path, "merged.vtr")
    result.save(output_file)
    print(f'Merged VTK files saved as {output_file}')

    return result

def merge_all_timesteps(data_path: str, output_path: str, num_cores: int = 8):
    """
    Merge VTK files for all timesteps in the simulation directory.

    Args:
        data_path (str): Path to the root directory of the simulation data.
        output_path (str): Path to the directory where merged data will be saved.
        num_cores (int): Number of cores to use for parallel processing.
    """
    sim_root = pathlib.Path(data_path)
    target_root = pathlib.Path(output_path)

    # Handle case where input and output paths are the same
    if sim_root == target_root:
        # Create a temporary directory with a unique name
        temp_dir = sim_root.parent / f"{sim_root.name}_temp_merge"
        target_root = temp_dir

    # Ensure output directory exists
    target_root.mkdir(parents=True, exist_ok=True)

    # Copy simulation directory structure without fluid VTK files
    copy_simulation_directories(sim_root, target_root)

    # Convert and merge VTK files
    convert_simulation_directories(sim_root, target_root, num_cores)

    # If we used a temporary directory, replace the original with the merged version
    if sim_root == pathlib.Path(output_path):
        # Remove the original directory
        shutil.rmtree(sim_root)
        # Rename the temporary directory to the original name
        target_root.rename(sim_root)

def copy_simulation_directories(source: pathlib.Path, destination: pathlib.Path):
    """
    Copy simulation directory tree without fluid VTK files.

    Args:
        source (pathlib.Path): Source directory path.
        destination (pathlib.Path): Destination directory path.
    """
    def ignore_vtk_files(dir, files):
        return [f for f in files if os.path.isfile(os.path.join(dir, f)) and f.endswith('.vtk')]

    shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore_vtk_files)

def convert_simulation_directories(input_path: pathlib.Path, output_path: pathlib.Path, num_cores: int):
    """
    Traverse the simulation directory tree and merge VTK files for all timesteps.

    Args:
        input_path (pathlib.Path): Input simulation directory.
        output_path (pathlib.Path): Output directory for merged data.
        num_cores (int): Number of cores to use for parallel processing.
    """
    sim_pattern = re.compile(r"(Fluid|localFluid)_p(?P<core>\d+)_t(?P<timestep>\d+).vtk")
    particle_pattern = re.compile(r"(Particles|Axes)_rank(?P<core>\d+)_t(?P<timestep>\d+).vtk")

    for root, _, files in tm.tqdm(os.walk(input_path), desc="Walking Simulation Directory tree", position=0):
        path = pathlib.Path(root)
        if path.name in ['VTKFluid', 'VTKLocalFluid', 'VTKParticles']:
            target_path = output_path / path.relative_to(input_path)
            target_path.mkdir(parents=True, exist_ok=True)

            if path.name == 'VTKFluid' or path.name == 'VTKLocalFluid':
                merge_vtk_files_in_directory(
                    path, target_path, sim_pattern, num_cores, data_type='fluid'
                )
            elif path.name == 'VTKParticles':
                merge_vtk_files_in_directory(
                    path, target_path, particle_pattern, num_cores, data_type='particle'
                )

def merge_vtk_files_in_directory(
    input_dir: pathlib.Path,
    output_dir: pathlib.Path,
    pattern: re.Pattern,
    num_cores: int,
    data_type: str = 'fluid'
):
    """
    Merge VTK files in a directory for all timesteps.

    Args:
        input_dir (pathlib.Path): Directory containing VTK files.
        output_dir (pathlib.Path): Directory to save merged VTK files.
        pattern (re.Pattern): Regex pattern to match VTK files.
        num_cores (int): Number of cores to use for parallel processing.
        data_type (str): Type of data ('fluid' or 'particle').
    """
    files = [f for f in os.listdir(input_dir) if f.endswith('.vtk')]
    timesteps = sorted(set(
        int(pattern.search(f).group('timestep')) for f in files if pattern.search(f)
    ))
    mpi_cores = max(
        int(pattern.search(f).group('core')) for f in files if pattern.search(f)
    ) + 1

    if data_type == 'fluid':
        merge_func = merge_fluid_timestep
    elif data_type == 'particle':
        merge_func = merge_particle_timestep
    else:
        raise ValueError("Invalid data_type. Must be 'fluid' or 'particle'.")

    jb.Parallel(n_jobs=num_cores, verbose=10)(
        jb.delayed(merge_func)(t, mpi_cores, input_dir, output_dir)
        for t in timesteps
    )

def merge_fluid_timestep(timestep: int, mpi_cores: int, input_dir: pathlib.Path, output_dir: pathlib.Path):
    """
    Merge fluid VTK files for a single timestep.

    Args:
        timestep (int): Timestep to merge.
        mpi_cores (int): Number of MPI cores.
        input_dir (pathlib.Path): Directory containing input VTK files.
        output_dir (pathlib.Path): Directory to save merged VTK file.
    """
    # Read and merge meshes
    meshes = []
    for core in range(mpi_cores):
        filename = input_dir / f"Fluid_p{core}_t{timestep}.vtk"
        if not filename.exists():
            continue
        mesh = pv.read(str(filename))
        meshes.append(mesh)
    if not meshes:
        return
    merged = meshes[0].merge(meshes[1:])

    # Interpolate onto a rectilinear grid
    x_min, x_max, y_min, y_max, z_min, z_max = merged.bounds
    x_lin = np.arange(x_min, x_max + 1, 1)
    y_lin = np.arange(y_min, y_max + 1, 1)
    z_lin = np.arange(z_min, z_max + 1, 1)
    grid = pv.RectilinearGrid(x_lin, y_lin, z_lin)
    result = grid.interpolate(merged)

    # Save the merged file
    output_file = output_dir / f"Fluid_t{timestep}.vtr"
    result.save(str(output_file))

def merge_particle_timestep(timestep: int, mpi_cores: int, input_dir: pathlib.Path, output_dir: pathlib.Path):
    """
    Merge particle VTK files for a single timestep.

    Args:
        timestep (int): Timestep to merge.
        mpi_cores (int): Number of MPI cores.
        input_dir (pathlib.Path): Directory containing input VTK files.
        output_dir (pathlib.Path): Directory to save merged VTK file.
    """
    # Read and merge meshes
    meshes = []
    for core in range(mpi_cores):
        filename = input_dir / f"Particles_rank{core}_t{timestep}.vtk"
        if not filename.exists():
            continue
        mesh = pv.read(str(filename))
        meshes.append(mesh)
    if not meshes:
        return
    merged = meshes[0].merge(meshes[1:])

    # Save the merged file
    output_file = output_dir / f"Particles_t{timestep}.vtp"
    merged.save(str(output_file))

# Additional utility functions can be added here as needed