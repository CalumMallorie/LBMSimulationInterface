import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom

class SimSetup:
    def __init__(self, folder_path):
        """
        Initializes the SimSetup object with the folder containing the parameter files.

        Args:
            folder_path (str): Path to the folder containing the parameter files.
        """
        self.folder_path = folder_path
        self.xml_paths = [os.path.join(folder_path, "parameters.xml"),
                          os.path.join(folder_path, "parametersMeshes.xml"),
                          os.path.join(folder_path, "parametersPositions.xml")]

    def prepare_and_run_simulation(self, directory_name, parameter_updates_by_file, num_cores=1, overwrite=False):
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
        FileSystem.create_directory(directory_name, overwrite)
        FileSystem.copy_file(os.path.join(self.folder_path, "LBCode"), directory_name)
        FileSystem.copy_directory(os.path.join(self.folder_path, "MeshGenerator"), directory_name)
        XmlBioFM.update_and_write_parameter_files(self.folder_path, directory_name, parameter_updates_by_file)
        self.execute_simulation(directory_name, num_cores)

    def execute_simulation(self, directory_name, num_cores):
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
            command = "./LBCode"
        else:
            command = f"mpiexec -n {num_cores} ./LBCode"
        os.system(command)

        # Restore the original working directory
        os.chdir(original_cwd)

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