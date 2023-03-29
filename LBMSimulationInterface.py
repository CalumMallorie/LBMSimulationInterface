import os
import shutil
import xml.etree.ElementTree as ET
import re
from xml.dom import minidom

class LBMSimulationInterface:
    def __init__(self, template_folder_path):
        self.template_folder_path = template_folder_path
        self.template_xml_paths = [os.path.join(template_folder_path, "parameters.xml"),
                           os.path.join(template_folder_path, "parametersMeshes.xml"),
                           os.path.join(template_folder_path, "parametersPositions.xml")]
        
    def read_template_xml(self, template_xml_path):
        """
        Reads the specified XML template file and returns a list of dictionaries representing the XML element hierarchy.

        Args:
            template_xml_path (str): Path to the XML template file.
        """
        with open(template_xml_path, 'r') as file:
            lines = file.readlines()
            # Skip the first line containing the XML declaration
            content = ''.join(lines[1:])

        # Add a temporary root element
        content = '<root>' + content + '</root>'
        root = ET.fromstring(content)

        # convert xml to list of dictionaries
        template_parameters = [self._xml_to_dict(parameter) for parameter in root]
        return template_parameters

    
    def calculate_new_parameters(self, template_parameters, parameter_updates):
        """
        Updates the given XML data structure with new values for specified parameters.

        Args:
            template_parameters (list): List of dictionaries representing the XML element hierarchy.
            parameter_updates (dict): Dictionary containing the XML element paths as keys and new values as values.
        """
        new_parameters = []
        for element_data in template_parameters:
            # Make a copy of the element_data dictionary to avoid modifying the original
            new_element_data = element_data.copy()
            for path, new_value in parameter_updates.items():
                # Update the element_data dictionary with new values
                self.update_parameter(new_element_data, path, new_value)
            new_parameters.append(new_element_data)
        return new_parameters#
        
    def write_new_parameter_file(self, directory_name, new_parameters, output_file_name):
        """
        Writes a new XML parameter file with the updated parameters.

        Args:
            directory_name (str): Name of the directory where the new parameter file will be written.
            new_parameters (list): List of dictionaries representing the updated XML element hierarchy.
            output_file_name (str): Name of the output XML file.
        """
        new_parameter_file_path = os.path.join(directory_name, output_file_name)

        # Create a temporary root element
        root = ET.Element("root")

        for param in new_parameters:
            element = self._dict_to_xml(param)
            root.append(element)

        # Convert the ElementTree to a string with pretty indentation
        xml_string = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="   ")

        # Remove the temporary root element and write the pretty XML to the file
        pretty_xml = pretty_xml.replace('<root>', '').replace('</root>', '').replace('<root/>', '')
        with open(new_parameter_file_path, 'w') as file:
            file.write(pretty_xml)

    def create_simulation_directory(self, directory_name):
        """
        Creates a new directory with the specified name if it doesn't already exist.

        Args:
            directory_name (str): Name of the new directory.
        """
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        return directory_name

    def copy_executable_to_directory(self, directory_name):
        """
        Copies the simulation executable to the specified directory.

        Args:
            directory_name (str): Name of the directory where the executable will be copied.
        """
        executable_name = "LBCode"
        source_executable = os.path.join(self.template_folder_path, executable_name)
        shutil.copy2(source_executable, os.path.join(directory_name, os.path.basename(source_executable)))
        # if os.path.exists(source_executable):
        #     shutil.copy2(source_executable, os.path.join(directory_name, os.path.basename(source_executable)))
        # else:
        #     print(f"Error: The simulation file {source_executable} does not exist.")

    def copy_mesh_generator_to_directory(self, directory_name):
        """
        Recursively copy the MeshGenerator folder to the specified directory.

        Args:
            directory_name (str): Name of the destination directory.
        """
        source_mesh_generator = os.path.join(self.template_folder_path, "MeshGenerator")
        destination_mesh_generator = os.path.join(directory_name, os.path.basename(source_mesh_generator))

        if os.path.exists(source_mesh_generator):
            shutil.copytree(source_mesh_generator, destination_mesh_generator)
        else:
            print(f"Error: The source MeshGenerator directory {source_mesh_generator} does not exist.")

    def run_simulation(self, directory_name, parameter_updates_by_filen, num_cores):
        """
        Runs the simulation in a new directory with the given name and updated parameters.
        The method handles multiple XML parameter files and updates the specified parameters in each file.

        Args:
            directory_name (str): Name of the new directory where the simulation will be run.
            parameter_updates_by_file (dict): Dictionary containing the XML file paths as keys, 
                                            and dictionaries with the XML element paths and new values as values.
        """
        self.create_simulation_directory(directory_name)
        self.copy_executable_to_directory(directory_name)
        self.copy_mesh_generator_to_directory(directory_name)

        # Prepend the template folder path to the keys in the parameter_updates_by_file dictionary
        full_path_parameter_updates_by_file = {os.path.join(self.template_folder_path, k): v for k, v in parameter_updates_by_file.items()}

        for template_xml_path, parameter_updates in full_path_parameter_updates_by_file.items():
            template_parameters = self.read_template_xml(template_xml_path)
            new_parameters = self.calculate_new_parameters(template_parameters, parameter_updates)

            output_file_name = os.path.basename(template_xml_path)
            self.write_new_parameter_file(directory_name, new_parameters, output_file_name)

        # Save the current working directory
        original_cwd = os.getcwd()

        # Change the working directory to the simulation directory
        os.chdir(directory_name)

        # Run the simulation with command depending on number of cores
        if num_cores == 1:
            command = "./LBCode"
        else:
            command = "mpiexec -n 8 ./LBCode"
        os.system(command)

        # Restore the original working directory
        os.chdir(original_cwd)

    def update_parameter(self,element, path, new_value):
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
                    self.update_parameter(child, path[1:], new_value)

    def _xml_to_dict(self, element):
        """
        Converts an XML element to a dictionary representation.

        Args:
            element (Element): An XML element.

        Returns:
            dict: A dictionary representing the XML element.
        """
        result = {"_tag": element.tag, "_attrib": element.attrib, "_children": []}
        for child in element:
            result["_children"].append(self._xml_to_dict(child))
        return result
    
    def _dict_to_xml(self, data):
        """
        Converts a dictionary representation of an XML element to an Element object.

        Args:
            data (dict): A dictionary representing an XML element.

        Returns:
            Element: An XML element.
        """
        element = ET.Element(data["_tag"], attrib=data["_attrib"])
        for child_data in data["_children"]:
            child = self._dict_to_xml(child_data)
            element.append(child)
        return element