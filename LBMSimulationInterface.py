import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import glob
import pyvista as pv
import re
import math
import subprocess
import json

def viscosity(tau):
    '''Calculates the lattice viscosity based on tau'''
    viscosity = (1/3)*(tau - 0.5)
    return viscosity

def grid_reynolds_check(tau, velocity):
    """
    Checks whether the grid Reynolds number is sufficiently small according to equation 7.18 in the LBM book
    """
    test_parameter = 0.5 + 0.125*velocity
    if tau < test_parameter:
        return True # fails the test
    else:
        return False # passes the test
    
def merging(datapath):
    # Find all files matching the pattern without specifying the timestep
    file_pattern = f"{datapath}Fluid_p*_t*.vtk"
    file_list = glob.glob(file_pattern)

    # Extract the timesteps from the filenames and find the largest timestep
    timesteps = [int(re.search(r"_t(\d+).vtk", f_name).group(1)) for f_name in file_list]
    largest_timestep = max(timesteps)

    # Update the file pattern using the largest timestep
    file_pattern = f"{datapath}Fluid_p*_t{largest_timestep}.vtk"
    file_list = glob.glob(file_pattern)

    # Sort the file list by core number using regex
    file_list.sort(key=lambda x: int(re.search(r"_p(\d+)_", x).group(1)))

    # Initialize an empty list to store the mesh objects
    meshes = []

    # Iterate through the sorted file list
    for f_name in file_list:
        # Read the VTK file and append the mesh object to the meshes list
        meshes.append(pv.read(f_name))

    # Merge the mesh objects in the meshes list and store the result
    merged = meshes[0].merge(meshes[1:])

    # Get the bounds of the merged mesh
    (x_min, x_max, y_min, y_max, z_min, z_max) = merged.bounds

    # Create equally spaced points along the x, y, and z axes
    x_lin = np.arange(x_min, x_max + 1, 1)
    y_lin = np.arange(y_min, y_max + 1, 1)
    z_lin = np.arange(z_min, z_max + 1, 1)

    # Create a rectilinear grid using the equally spaced points
    grid = pv.RectilinearGrid(x_lin, y_lin, z_lin)

    # Interpolate the merged mesh onto the rectilinear grid
    result = grid.interpolate(merged)

    # Return the interpolated grid
    return result

class ParameterUpdates:
    def __init__(self, parameter_updates=None):
        if parameter_updates is None:
            self.parameter_updates = {
                "parameters.xml": {},
                "parametersMeshes.xml": {},
                "parametersPositions.xml": {}
            }
        else:
            self.parameter_updates = parameter_updates

    def MPI(self, mpi):
        self.parameter_updates["parameters.xml"].update({
            ('MPI', 'cores', 'x'): str(mpi[0]),
            ('MPI', 'cores', 'y'): str(mpi[1]),
            ('MPI', 'cores', 'z'): str(mpi[2]),
        })

    def lattice(self, lattice_NX, lattice_NY, lattice_NZ):
        self.parameter_updates["parameters.xml"].update({
            ('lattice', 'size', 'NX'): str(lattice_NX),
            ('lattice', 'size', 'NY'): str(lattice_NY),
            ('lattice', 'size', 'NZ'): str(lattice_NZ),
        })

    def sim_time(self, t_end):
        self.parameter_updates["parameters.xml"].update({
            ('lattice', 'times', 'end'): str(t_end),
        })

    def info_time(self, t_info):
        self.parameter_updates["parameters.xml"].update({
            ('lattice', 'times', 'info'): str(t_info),
        })

    def checkpoint(self, step, restartLBM, restartMEM):
        self.parameter_updates["parameters.xml"].update({
                    ('checkpoint','save', 'step'): str(step),
                    ('checkpoint','restart','timeLBM'): str(restartLBM),
                    ('checkpoint','restart','timeMEM'): str(restartMEM),
                    })

    def relaxation(self, tau):
        self.parameter_updates["parameters.xml"].update({
            ('LBM','relaxation', 'tau'): str(tau),
        })

    def MRT(self, tauBulk, magic):
        self.parameter_updates["parameters.xml"].update({
            ('LBM', 'MRT', 'active'): "1",
            ('LBM', 'MRT', 'tauBulk'): str(tauBulk),
            ('LBM', 'MRT', 'Lambda'): str(magic),
        })

    def cross_slot_geometry(self, inlet_width, outlet_width, stenosis_width, stenosis_length):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'CrossSlot', 'active'): "1",
            ('boundaries', 'CrossSlot', 'inletWidth'): str(inlet_width),
            ('boundaries', 'CrossSlot', 'outletWidth'): str(outlet_width),
            ('boundaries', 'CrossSlot', 'stenosisWidth'): str(stenosis_width),
            ('boundaries', 'CrossSlot', 'stenosisLength'): str(stenosis_length),
        })

    def cross_slot_velocity(self, inlet_velocity):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'CrossSlot', 'inletVelocity'): str(inlet_velocity),
        })

    def cross_slot_vortex(self, vortex_force_mag, vortex_time_begin, vortex_time_end):
        self.parameter_updates["parameters.xml"].update({
            ('boundaries', 'CrossSlot', 'ForceTriggerMagnitude'): str(vortex_force_mag),
            ('boundaries', 'CrossSlot', 'TimeBegin'): str(vortex_time_begin),
            ('boundaries', 'CrossSlot', 'TimeEnd'): str(vortex_time_end),
        })

    def convergence(self, time_ignore, convergence):
        self.parameter_updates["parameters.xml"].update({
            ('convergence', 'steady', 'active'): "1",
            ('convergence', 'steady', 'timeIgnore'): str(time_ignore),
            ('convergence', 'steady', 'timeInterval'): "1000",
            ('convergence', 'steady', 'threshold'): str(convergence),
        })

    def no_convergence(self):
        self.parameter_updates["parameters.xml"].update({
            ('convergence', 'steady', 'active'): "0",
        })

    def mesh_viscosity_contrast(self, viscosity_ratio):
        self.parameter_updates["parametersMeshes.xml"].update({
            ('viscosityContrast', 'indexField', 'active'): "1",
            ('viscosityContrast', 'viscosity', 'ratio'): str(viscosity_ratio),
        })

    def mesh(self, radius=0, kV=0, kA=0, kalpha=0, kS=0, kB=0, density=0, shearViscosity=0, dilationalViscosity=0, kmaxwell_dilation=0, kmaxwell_shear=0):
        self.parameter_updates["parametersMeshes.xml"].update({
            ('mesh', 'general', 'radius'): str(radius),
            ('mesh', 'general', 'file'): f"./MeshGenerator/sph_ico_{20*math.ceil(radius*1.2)**2}.msh",
            ('mesh', 'physics', 'kV'): str(kV),
            ('mesh', 'physics', 'kA'): str(kA),
            ('mesh', 'physics', 'kalpha'): str(kalpha),
            ('mesh', 'physics', 'kS'): str(kS),
            ('mesh', 'physics', 'kB'): str(kB),
            ('mesh', 'physics', 'density'): str(density),
            ('mesh', 'physics', 'ShearViscosity'): str(shearViscosity),
            ('mesh', 'physics', 'DilationalViscosity'): str(dilationalViscosity),
            ('mesh', 'physics', 'kMaxwell_dilation'): str(kmaxwell_dilation),
            ('mesh', 'physics', 'kMaxwell_shear'): str(kmaxwell_shear),
        })

    def mesh_positions(self, position, angle="0", axisX="1", axisY="1", axisZ="1"):
        self.parameter_updates["parametersPositions.xml"].update({
            ('particle', 'X'): str(position[0]),
            ('particle', 'Y'): str(position[1]),
            ('particle', 'Z'): str(position[2]),
            ('particle', 'angle'): str(angle),
            ('particle', 'axisX'): str(axisX),
            ('particle', 'axisY'): str(axisY),
            ('particle', 'axisZ'): str(axisZ),
        })

    def get_parameter_updates(self):
        return self.parameter_updates


class SimSetup:
    def __init__(self, template_path, root_path):
        """
        Initializes the SimSetup object with the folder containing the parameter files.

        Args:
            folder_path (str): Path to the folder containing the parameter files.
        """
        self.template_path = template_path
        self.root_path = root_path

    def prepare_and_run_simulation(self, parameter_updates_by_file, num_cores=1, overwrite=False, checkpoint=False, logfile=None):
        """
        Runs the simulation in a new directory with the given name and updated parameters.
        The method handles multiple XML parameter files and updates the specified parameters in each file.

        Args:
            directory_name (str): Name of the new directory where the simulation will be run.
            parameter_updates_by_file (dict): Dictionary containing the XML file paths as keys, 
                                            and dictionaries with the XML element paths and new values as values.
            num_cores (int, optional): Number of cores to use for the simulation. Defaults to 1.
            overwrite (bool, optional): If True, overwrite the previous simulation attempt. Defaults to False.
        """
        
        FileSystem.create_root(self.root_path)
        simulation_ID = FileSystem.get_next_ID(os.path.join(self.root_path, "simulation_lookup.json"))
        directory_name = os.path.join(self.root_path, str(simulation_ID))
        
        FileSystem.create_directory(directory_name, overwrite)
        FileSystem.copy_file(os.path.join(self.template_path, "LBCode"), directory_name)
        FileSystem.copy_directory(os.path.join(self.template_path, "MeshGenerator"), directory_name)
        if checkpoint:
            FileSystem.copy_directory(os.path.join(self.template_path, "Backup"), directory_name)
        XmlBioFM.update_and_write_parameter_files(self.template_path, directory_name, parameter_updates_by_file)
        exit_code = self.execute_simulation(directory_name, num_cores, logfile)
        
        return exit_code

    def execute_simulation(self, directory_name, num_cores, logfile):
        """
        Executes the simulation in the specified directory.

        Args:
            directory_name (str): Name of the directory where the simulation will be run.
            num_cores (int): Number of cores to use for the simulation.
        """
        # Save the current working directory
        original_cwd = os.getcwd()

        # Change the working directory to the simulation directory
        os.chdir(directory_name)

        # Run the simulation with command depending on number of cores
        if num_cores == 1:
            command = ["./LBCode"]
        else:
            command = ["mpiexec", "-n", str(num_cores), "./LBCode"]

        if logfile:
            with open(logfile, 'w') as f:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                for line in iter(process.stdout.readline, b''):
                    f.write(line.decode())
                    f.flush()  # This line ensures that the file is written to disk after each line

                process.stdout.close()
                exit_code = process.wait()
        else:
            process = subprocess.Popen(command)
            exit_code = process.wait()

        # Restore the original working directory
        os.chdir(original_cwd)

        return exit_code

class FileSystem:
    @staticmethod
    def create_directory(directory_name, overwrite=False):
        """
        Creates a new directory with the specified name if it doesn't already exist.

        Args:
            directory_name (str): Name of the new directory.
            overwrite (bool): If True, overwrite the previous simulation attempt.
        """
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        elif overwrite:
            shutil.rmtree(directory_name)
            os.makedirs(directory_name)

    @staticmethod
    def copy_file(source_file, destination_directory):
        """
        Copies a file to the specified directory.

        Args:
            source_file (str): Path to the source file.
            destination_directory (str): Path to the destination directory.
        """
        shutil.copy2(source_file, os.path.join(destination_directory, os.path.basename(source_file)))

    @staticmethod
    def copy_directory(source_directory, destination_directory):
        """
        Recursively copy a source directory to the specified destination directory.

        Args:
            source_directory (str): Path to the source directory.
            destination_directory (str): Path to the destination directory.
        """
        destination = os.path.join(destination_directory, os.path.basename(source_directory))

        if os.path.exists(source_directory):
            shutil.copytree(source_directory, destination)
        else:
            print(f"Error: The source directory {source_directory} does not exist.")

    @staticmethod
    def create_root(root_directory):
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)
            simulation_lookup_path = root_directory + "simulation_lookup.json"
            # with open(simulation_lookup_path, 'w') as lookup_file:
            #     json.dump({}, lookup_file)  # Create an empty JSON object to start

    @staticmethod
    def get_next_ID(lookup_file):
        # If the file does not exist, return 0
        if not os.path.isfile(lookup_file):
            return 0
        else:
            # Open the file and find the maximum Simulation ID
            with open(lookup_file, 'r') as infile:
                lookup_data = json.load(infile)
                return max(map(int, lookup_data.keys())) + 1  # Find the max Simulation ID and add 1 to it


    @staticmethod
    def update_json(root_directory, parameters_dictionary, exit_code):
        lookup_file = os.path.join(root_directory, "simulation_lookup.json")

        # Get the next simulation ID
        simulation_ID = FileSystem.get_next_ID(lookup_file)

        # If the file does not exist, create it with an empty dictionary
        if simulation_ID == 0:
            with open(lookup_file, 'w') as outfile:
                json.dump({}, outfile)

        # Open the file and add the new simulation data
        with open(lookup_file, 'r+') as f:
            lookup_data = json.load(f)
            lookup_data[str(simulation_ID)] = {"Simulation ID": simulation_ID, "Parameters": parameters_dictionary, "Exit code": exit_code}  # Add new entry
            f.seek(0)  # Move file pointer to beginning
            json.dump(lookup_data, f, indent=4)
            f.truncate()  # Delete anything that's left after the new JSON object

        # Write the parameters to a simulation_info.json file in the simulation folder
        simulation_subfolder = os.path.join(root_directory, str(simulation_ID))
        simulation_info_path = os.path.join(simulation_subfolder, "simulation_info.json")
        with open(simulation_info_path, 'w') as info_file:
            json.dump({"Simulation ID": simulation_ID, "Parameters": parameters_dictionary}, info_file, indent=4)


class XmlBioFM:
    @staticmethod
    def read_xml_file(xml_file_path):
        """
        Reads the XML file and returns a list of dictionaries representing the file's content.

        Args:
            xml_file_path (str): Path to the XML file.

        Returns:
            list: List of dictionaries representing the XML content.
        """
        with open(xml_file_path, 'r') as file:
            lines = file.readlines()
            # Skip the first line containing the XML declaration
            content = ''.join(lines[1:])

        # Add a temporary root element
        content = '<root>' + content + '</root>'
        root = ET.fromstring(content)

        # convert xml to list of dictionaries
        parameters = [XmlBioFM._xml_to_dict(parameter) for parameter in root]
        return parameters

    @staticmethod
    def calculate_new_parameters(parameters, parameter_updates):
        """
        Calculates the new parameters by updating the existing ones.

        Args:
            parameters (list): List of dictionaries representing the XML content.
            parameter_updates (dict): Dictionary containing the XML element paths and new values as values.

        Returns:
            list: List of dictionaries representing the updated XML content.
        """
        new_parameters = []
        for element_data in parameters:
            # Make a copy of the element_data dictionary to avoid modifying the original
            new_element_data = element_data.copy()
            for path, new_value in parameter_updates.items():
                # Update the element_data dictionary with new values
                XmlBioFM.update_parameter(new_element_data, path, new_value)
            new_parameters.append(new_element_data)
        return new_parameters

    @staticmethod
    def update_parameter(element, path, new_value):
        """
        Recursively updates the attribute value of an XML element based on the given path.

        Args:
            element (dict): The current XML element represented as a dictionary, with keys "_tag", "_attrib", and "_children".
            path (list of str): A list of strings representing the XML element path. The last item in the path should be the attribute name.
            new_value (str): The new value to set for the specified attribute.

        Example:
            Given an XML element structure like this:
            <parent>
                <child attribute="value"/>
            </parent>

            To update the "attribute" value of the "child" element, the method should be called as follows:
            update_parameter(parent_element, ["child", "attribute"], "new_value")
        """
        # Return if there are no path elements left
        if not path:
            return

        # Check if the current element's tag matches the first item in the path
        if element["_tag"] == path[0]:
            if len(path) == 2:
                # If the path has only one more item, update the attribute value
                element["_attrib"][path[1]] = new_value
            else:
                # Otherwise, recursively update the child elements
                for child in element["_children"]:
                    XmlBioFM.update_parameter(child, path[1:], new_value)

    @staticmethod
    def write_new_parameter_file(directory_name, new_parameters, output_file_name):
        """
        Writes the new parameter file to the specified directory.

        Args:
            directory_name (str): Path to the directory where the file will be written.
            new_parameters (list): List of dictionaries representing the updated XML content.
            output_file_name (str): Name of the output file.
        """
        new_parameter_file_path = os.path.join(directory_name, output_file_name)
        
        # Create a temporary root element
        root = ET.Element("root")

        for param in new_parameters:
            element = XmlBioFM._dict_to_xml(param)
            root.append(element)

        # Convert the ElementTree to a string with pretty indentation
        xml_string = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="   ")

        # Remove the temporary root element and write the pretty XML to the file
        pretty_xml = pretty_xml.replace('<root>', '').replace('</root>', '').replace('<root/>', '')
        with open(new_parameter_file_path, 'w') as file:
            file.write(pretty_xml)

    @staticmethod
    def update_and_write_parameter_files(folder_path, directory_name, parameter_updates_by_file):
        """
        Updates parameter files and writes them to the specified directory.

        Args:
            folder_path (str): Path to the folder containing the source parameter files.
            directory_name (str): Path to the folder where the updated parameter files will be written.
            parameter_updates_by_file (dict): Dictionary containing the XML file paths as keys,
                                              and dictionaries with the XML element paths and new values as values.
        """
        # Prepend the template folder path to the keys in the parameter_updates_by_file dictionary
        full_path_parameter_updates_by_file = {os.path.join(folder_path, k): v for k, v in parameter_updates_by_file.items()}

        # Write the new parameter files into the simulation directory
        for xml_path, parameter_updates in full_path_parameter_updates_by_file.items():
            parameters = XmlBioFM.read_xml_file(xml_path)
            new_parameters = XmlBioFM.calculate_new_parameters(parameters, parameter_updates)

            output_file_name = os.path.basename(xml_path)
            XmlBioFM.write_new_parameter_file(directory_name, new_parameters, output_file_name)

    @staticmethod
    def _xml_to_dict(element):
        """
        Converts an XML element to a dictionary.

        Args:
            element (Element): An XML element.

        Returns:
            dict: A dictionary representing the XML element.
        """
        result = {"_tag": element.tag, "_attrib": element.attrib, "_children": []}
        for child in element:
            result["_children"].append(XmlBioFM._xml_to_dict(child))
        return result

    @staticmethod
    def _dict_to_xml(data):
        """
        Converts a dictionary to an XML element.

        Args:
            data (dict): A dictionary representing the XML element.

        Returns:
            Element: An XML element.
        """
        element = ET.Element(data["_tag"], attrib=data["_attrib"])
        for child_data in data["_children"]:
            child = XmlBioFM._dict_to_xml(child_data)
            element.append(child)
        return element