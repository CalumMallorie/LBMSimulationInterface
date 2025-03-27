# file_system.py

import os
import shutil
import json
from pathlib import Path
from typing import Dict, Any

class FileSystem:
    """
    Class for handling file system operations.
    """

    @staticmethod
    def create_directory(directory_name: str, overwrite: bool = False) -> None:
        """
        Create a new directory.

        Args:
            directory_name (str): Name of the directory.
            overwrite (bool): Overwrite if directory exists.
        """
        path = Path(directory_name)
        if not path.exists():
            path.mkdir(parents=True)
        elif overwrite:
            shutil.rmtree(path)
            path.mkdir(parents=True)

    @staticmethod
    def copy_file(source_file: str, destination_directory: str) -> None:
        """
        Copy a file to a destination directory.

        Args:
            source_file (str): Path to the source file.
            destination_directory (str): Path to the destination directory.
        """
        destination = Path(destination_directory) / Path(source_file).name
        shutil.copy2(source_file, destination)

    @staticmethod
    def copy_directory(source_directory: str, destination_directory: str) -> None:
        """
        Copy a directory recursively.

        Args:
            source_directory (str): Path to the source directory.
            destination_directory (str): Path to the destination directory.
        """
        destination = Path(destination_directory) / Path(source_directory).name
        if Path(source_directory).exists():
            shutil.copytree(source_directory, destination)
        else:
            raise FileNotFoundError(f"Source directory {source_directory} not found.")

    @staticmethod
    def create_root(root_directory: str) -> None:
        """
        Create the root directory if it doesn't exist.

        Args:
            root_directory (str): Path to the root directory.
        """
        path = Path(root_directory)
        if not path.exists():
            path.mkdir(parents=True)

    @staticmethod
    def get_next_ID(lookup_file: str) -> int:
        """
        Get the next simulation ID.

        Args:
            lookup_file (str): Path to the simulation lookup JSON file.

        Returns:
            int: Next simulation ID.
        """
        if not Path(lookup_file).is_file():
            return 0
        else:
            with open(lookup_file, 'r') as infile:
                lookup_data = json.load(infile)
                return max(map(int, lookup_data.keys())) + 1

    @staticmethod
    def update_json(root_directory: str,
                    parameters_dictionary: Dict[str, Any],
                    exit_code: int) -> None:
        """
        Update the simulation lookup JSON file.

        Args:
            root_directory (str): Path to the root directory.
            parameters_dictionary (Dict[str, Any]): Parameters used in the simulation.
            exit_code (int): Exit code of the simulation.
        """
        lookup_file = Path(root_directory) / "simulation_lookup.json"
        simulation_ID = FileSystem.get_next_ID(str(lookup_file))

        if simulation_ID == 0:
            with open(lookup_file, 'w') as outfile:
                json.dump({}, outfile)
        with open(lookup_file, 'r+') as f:
            lookup_data = json.load(f)
            lookup_data[str(simulation_ID)] = {
                "Simulation ID": simulation_ID,
                "Parameters": parameters_dictionary,
                "Exit code": exit_code
            }
            f.seek(0)
            json.dump(lookup_data, f, indent=4)
            f.truncate()

        # Write simulation info to a file in the simulation directory
        simulation_subfolder = Path(root_directory) / str(simulation_ID)
        simulation_info_path = simulation_subfolder / "simulation_info.json"
        with open(simulation_info_path, 'w') as info_file:
            json.dump({
                "Simulation ID": simulation_ID,
                "Parameters": parameters_dictionary
            }, info_file, indent=4)
        
    @staticmethod
    def check_simulation_exists(root_directory: str, parameter_updates: Dict[str, Any]) -> bool:
        """
        Check if any simulation with matching parameters exists in the lookup json.
        If found, verify consistency with simulation_info.json.

        Args:
            root_directory: Root directory containing simulation data
            parameter_updates: Dictionary of parameter updates to match against

        Returns:
            bool: True if matching simulation exists and is consistent

        Raises:
            ValueError: If simulation found in lookup but mismatch in simulation_info.json
        """
        lookup_file = Path(root_directory) / "simulation_lookup.json"
        
        # Find matching simulation by parameters
        matching_simulation_id = None
        with open(lookup_file, 'r') as infile:
            lookup_data = json.load(infile)
            for simulation_id, simulation_info in lookup_data.items():
                if simulation_info["Parameters"] == parameter_updates:
                    matching_simulation_id = simulation_id
                    break
        
        if matching_simulation_id is None:
            return False
        
        # Verify consistency with simulation_info.json
        simulation_subfolder = Path(root_directory) / str(matching_simulation_id)
        simulation_info_path = simulation_subfolder / "simulation_info.json"
        
        with open(simulation_info_path, 'r') as info_file:
            simulation_info = json.load(info_file)
            if simulation_info["Parameters"] != parameter_updates:
                raise ValueError(f"Simulation {matching_simulation_id} found in lookup json but mismatch in simulation_info.json")
        
        return True


