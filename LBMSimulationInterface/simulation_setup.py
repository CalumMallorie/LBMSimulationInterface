# simulation_setup.py

import os
import json
import subprocess
from typing import Optional
from .file_system import FileSystem
from .xml_handler import XmlBioFM
from .parameter_updates import ParameterUpdates


class SimulationSetup:
    """
    Class to prepare and execute simulations.
    """

    def __init__(
        self,
        template_path: str,
        root_path: str,
        parameter_updates: ParameterUpdates,
        simulation_id: Optional[int] = None,
        overwrite: bool = False,
    ):
        """
        Initialize the SimulationSetup object and prepare the simulation.

        Args:
            template_path (str): Path to the template files.
            root_path (str): Root path for simulations.
            parameter_updates (ParameterUpdates): Parameter updates.
            simulation_id (Optional[int]): Specific simulation ID.
            overwrite (bool): Overwrite existing simulation directory.
        """
        self.template_path = template_path
        self.root_path = root_path
        self.parameter_updates = parameter_updates
        self.simulation_id = simulation_id
        self.overwrite = overwrite
        self.simulation_directory = self.prepare_simulation()

    def prepare_simulation(self) -> str:
        """
        Prepare the simulation directory and parameter files.

        Returns:
            str: Path to the simulation directory.
        """
        FileSystem.create_root(self.root_path)

        if self.simulation_id is None:
            self.simulation_id = FileSystem.get_next_ID(
                os.path.join(self.root_path, "simulation_lookup.json")
            )
        directory_name = os.path.join(self.root_path, str(self.simulation_id))

        FileSystem.create_directory(directory_name, self.overwrite)
        FileSystem.copy_file(os.path.join(self.template_path, "LBCode"), directory_name)
        FileSystem.copy_directory(
            os.path.join(self.template_path, "MeshGenerator"), directory_name
        )
        if os.path.exists(os.path.join(self.template_path, "Backup")):
            FileSystem.copy_directory(os.path.join(self.template_path, "Backup"), directory_name)
        # Update and write parameter files
        XmlBioFM.update_and_write_parameter_files(
            self.template_path,
            directory_name,
            self.parameter_updates.get_parameter_updates(),
        )
        # FileSystem.update_json(self.root_path, self.parameter_updates.get_parameter_updates(), 0)
        return directory_name

    def run_simulation(
        self, num_cores: int = 1, logfile: Optional[str] = None
    ) -> int:
        """
        Execute the simulation in the specified directory.

        Args:
            num_cores (int): Number of cores to use.
            logfile (Optional[str]): Path to the logfile.

        Returns:
            int: Exit code of the simulation process.
        """
        original_cwd = os.getcwd()
        os.chdir(self.simulation_directory)

        command = (
            ["./LBCode"]
            if num_cores == 1
            else ["mpiexec", "-n", str(num_cores), "./LBCode"]
        )

        if logfile:
            with open(logfile, "w") as f:
                process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                for line in iter(process.stdout.readline, b""):
                    f.write(line.decode())
                    f.flush()
                process.stdout.close()
                exit_code = process.wait()
        else:
            process = subprocess.Popen(command)
            exit_code = process.wait()

        os.chdir(original_cwd)
        return exit_code
