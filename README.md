# LBMSimulationInterface

A Python interface for setting up and running Lattice-Boltzmann Method (LBM) simulations with BioFM's LBM solver (`LBCode`).

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Installing the Package](#installing-the-package)
- [Usage](#usage)
  - [Setting Up a Simulation Study](#setting-up-a-simulation-study)
  - [Writing the Main Simulation Script](#writing-the-main-simulation-script)
  - [Running Simulations](#running-simulations)
  - [Example Simulation Script](#example-simulation-script)
- [Package Components](#package-components)
  - [SimulationSetup Class](#simulationsetup-class)
  - [ParameterUpdates Class](#parameterupdates-class)
  - [Physics Utilities](#physics-utilities)
  - [VTK Utilities](#vtk-utilities)
- [License](#license)

---

## Introduction

**LBMSimulationInterface** is a Python package designed to streamline the process of setting up and running Lattice-Boltzmann Method (LBM) simulations using BioFM's `LBCode`. It provides a programmatic interface for generating and modifying XML parameter files, automating simulation runs, and performing parameter sweeps over physical quantities like Reynolds and Capillary numbers.

This package aims to simplify the simulation setup process, especially for users who may not have extensive experience with Python or programming. By abstracting away the complexities of file handling and parameter management, researchers can focus on the physics and analysis of their simulations.

---

## Features

- **Easy Simulation Setup**: Programmatically generate and modify simulation parameter files.
- **Automation**: Automate the preparation and execution of simulations, including parameter sweeps.
- **Physical Parameter Specification**: Define simulations using physical parameters (e.g., Reynolds number) instead of arbitrary simulation quantities.
- **Multiple Simulation Studies**: Organize and manage multiple simulation campaigns with separate templates and data directories.
- **Modular Design**: Components are modular and reusable, making it easy to extend functionality.
- **VTK File Merging**: Merge VTK files from parallel simulations, both for the latest timestep and all timesteps in a simulation directory.

---

## Project Structure

The typical directory structure for the project is as follows:
```
project_root/
├── LBMSimulationInterface/
│   ├── init.py
│   ├── file_system.py
│   ├── parameter_updates.py
│   ├── simulation_setup.py
│   ├── vtk_utils.py
│   ├── physics_utils.py
│   ├── xml_handler.py
│   └── lbm_utils.py
├── setup.py
├── requirements.txt
├── study1/
│   ├── main.py
│   ├── template/
│   │   ├── LBCode
│   │   ├── MeshGenerator/
│   │   ├── parameters.xml
│   │   ├── parametersMeshes.xml
│   │   └── parametersPositions.xml
│   └── simulations/
├── study2/
│   ├── main.py
│   ├── template/
│   └── simulations/
└── …
```

- **LBMSimulationInterface/**: The Python package containing the simulation interface code.
- **setup.py**: Installation script for the package.
- **requirements.txt**: Lists the dependencies required by the project.
- **studyX/**: Directories for individual simulation studies, each with its own `main.py`, templates, and simulations.



## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` package installer
- `numpy` and `pyvista` libraries

### Cloning the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/LBMSimulationInterface.git
cd LBMSimulationInterface
```

## Setting up a virtual environment 
It is recommended to use a virtual environment to manage dependencies:
```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment (Unix/Linux)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

## Installing the package
Install the package and it's dependencies:
```bash
pip install -e .
```
This installs the package in editable mode, allowing changes to the code to take effect without reinstallation.

Alternatively, install the dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage
### Setting up a simulation study:
Create a new directory for your simulation study:

```bash
mkdir study1
cd study1
```

Within this directory, create the following structure:
```
study1/
├── main.py
├── template/
└── simulations/
```

- **main.py**: Your simulation script.
- **template/**: Contains LBCode, MeshGenerator/, and the template XML parameter files.
- **simulations/**: Will store simulation outputs.

## Writing the main simulation script

In the `main.py`, you will:

- Import necessary classes from LBMSimulationInterface.
- Define physical parameters for your simulations.
- Set up parameter updates using ParameterUpdates.
- Initialize SimulationSetup with the template path, simulations root, and parameter updates.
- Run the simulations.

## Running simulations

Run your simulation script:
```bash
python main.py
```

This will:

- Prepare simulation directories and parameter files.
- Execute simulations based on the defined parameters.
- Store outputs in the simulations/ directory.

## Example simulation script 

```python
# main.py

from LBMSimulationInterface import SimulationSetup, ParameterUpdates
import os

def main():
    # Define paths
    study_dir = os.path.dirname(__file__)
    template_path = os.path.join(study_dir, 'template')
    simulations_root = os.path.join(study_dir, 'simulations')

    # Simulation parameters
    Re_values = [10, 50, 100]
    Ca_values = [0.01, 0.1, 1.0]

    for Re in Re_values:
        for Ca in Ca_values:
            # Unique simulation ID
            sim_id = f'Re={Re}_Ca={Ca}'
            print(f"Starting simulation {sim_id}")

            # Parameter updates
            param_updates = ParameterUpdates()
            param_updates.lattice(NX=100, NY=100, NZ=100)
            param_updates.sim_time(t_end=10000)
            param_updates.MPI((2, 2, 2))
            # Additional parameter updates based on Re and Ca

            # Initialize SimulationSetup
            sim_setup = SimulationSetup(
                template_path=template_path,
                root_path=simulations_root,
                parameter_updates=param_updates,
                overwrite=True,
                simulation_id=sim_id
            )

            # Run simulation
            exit_code = sim_setup.run_simulation(num_cores=4, logfile=f'{sim_id}.log')
            print(f"Simulation {sim_id} finished with exit code {exit_code}")

if __name__ == '__main__':
    main()
```

## Package components
### SimulationSetup class
-**Purpose**: Prepares simulation directories, copies necessary files, updates parameter files, and runs simulations.
-**Usage**: 
```python
sim_setup = SimulationSetup(
    template_path='path/to/template',
    root_path='path/to/simulations',
    parameter_updates=param_updates,
    overwrite=True,
    simulation_id='unique_sim_id'
)
```
-**Methods**: 
`run_simulation(num_cores=1, logfile=None)`: Executes the simulation.

### ParameterUpdates class
-**Purpose**:  Manages updates to simulation parameter XML files.
```python
param_updates = ParameterUpdates()
param_updates.lattice(NX=100, NY=100, NZ=100)
param_updates.sim_time(t_end=10000)
```
-**Methods**: 
Each section in the .xml parameter files will have it's own method in the `ParameterUpdates` class, e.g. `lattice(NX, NY, NZ)` sets the lbm lattice size.
Currently, there is not an exhaustive set of these methods, as I have only added those which I use. 
I expect that any user of this library will add their own methods to the class for their own purposes.

### LBM utilities
-**Module**: `lbm_utils.py`
-**Useage**: This module contains functions to carry out numerical 'sanity checks', which are numerous in LBM uses. 
A good example of this is the `check_grid_reynolds_number(tau, velocity)` function, which computes the grid Reynolds number, which must be sufficiently low for stable LBM simulations.

### VTK utilities
-**Module**: `vtk_utils.py`
-**Functions**:
- `merge_latest_fluid_vtk_files(data_path)`: Merges VTK files for the latest timestep.
- `merge_all_timesteps(data_path, output_path, num_cores=8)`: Merges VTK files for all timesteps in a simulation directory.

## License
This project is licensed under the MIT License.
