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
  - [FileSystem Class](#filesystem-class)
  - [XmlBioFM Class](#xmlbiofm-class)
  - [Physics Utilities](#physics-utilities)
  - [VTK Utilities](#vtk-utilities)
- [Troubleshooting](#troubleshooting)
- [Additional Notes](#additional-notes)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

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

