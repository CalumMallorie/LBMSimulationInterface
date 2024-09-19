# xml_handler.py

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Tuple, Any, List

class XmlBioFM:
    """
    Class to handle reading, updating, and writing XML parameter files.
    """

    @staticmethod
    def read_xml_file(xml_file_path: str) -> List[Dict[str, Any]]:
        """
        Read an XML file and return its content as a list of dictionaries.

        Args:
            xml_file_path (str): Path to the XML file.

        Returns:
            List[Dict[str, Any]]: List of dictionaries representing XML elements.
        """
        with open(xml_file_path, 'r') as file:
            lines = file.readlines()
            # Skip the first line containing the XML declaration
            content = ''.join(lines[1:])

        # Add a temporary root element
        content = '<root>' + content + '</root>'
        root = ET.fromstring(content)

        parameters = [XmlBioFM._xml_to_dict(element) for element in root]
        return parameters

    @staticmethod
    def calculate_new_parameters(
            parameters: List[Dict[str, Any]],
            parameter_updates: Dict[Tuple[str, ...], Any]) -> List[Dict[str, Any]]:
        """
        Update existing parameters with new values.

        Args:
            parameters (List[Dict[str, Any]]): Existing parameters.
            parameter_updates (Dict[Tuple[str, ...], Any]): Updates to apply.

        Returns:
            List[Dict[str, Any]]: Updated parameters.
        """
        for path, new_value in parameter_updates.items():
            for element_data in parameters:
                XmlBioFM.update_parameter(element_data, list(path), new_value)
        return parameters

    @staticmethod
    def update_parameter(element: Dict[str, Any],
                         path: List[str],
                         new_value: Any) -> None:
        """
        Recursively update the attribute value of an XML element.

        Args:
            element (Dict[str, Any]): XML element as a dictionary.
            path (List[str]): Path to the attribute.
            new_value (Any): New value to set.
        """
        if not path:
            return
        if element["_tag"] == path[0]:
            if len(path) == 2:
                element["_attrib"][path[1]] = new_value
            else:
                for child in element["_children"]:
                    XmlBioFM.update_parameter(child, path[1:], new_value)

    @staticmethod
    def write_new_parameter_file(directory_name: str,
                                 new_parameters: List[Dict[str, Any]],
                                 output_file_name: str) -> None:
        """
        Write the updated parameters to an XML file.

        Args:
            directory_name (str): Path to the output directory.
            new_parameters (List[Dict[str, Any]]): Updated parameters.
            output_file_name (str): Name of the output file.
        """
        new_parameter_file_path = os.path.join(directory_name, output_file_name)
        root = ET.Element("root")

        for param in new_parameters:
            element = XmlBioFM._dict_to_xml(param)
            root.append(element)

        xml_string = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="   ")

        # Remove the temporary root element
        pretty_xml = pretty_xml.replace('<root>', '').replace('</root>', '').strip()
        with open(new_parameter_file_path, 'w') as file:
            file.write(pretty_xml)

    @staticmethod
    def update_and_write_parameter_files(
            template_path: str,
            directory_name: str,
            parameter_updates_by_file: Dict[str, Dict[Tuple[str, ...], Any]]) -> None:
        """
        Update parameter files and write them to the output directory.

        Args:
            template_path (str): Path to the template files.
            directory_name (str): Path to the output directory.
            parameter_updates_by_file (Dict[str, Dict[Tuple[str, ...], Any]]): Updates.
        """
        full_path_updates = {
            os.path.join(template_path, k): v
            for k, v in parameter_updates_by_file.items()
        }

        for xml_path, parameter_updates in full_path_updates.items():
            parameters = XmlBioFM.read_xml_file(xml_path)
            new_parameters = XmlBioFM.calculate_new_parameters(
                parameters, parameter_updates)
            output_file_name = os.path.basename(xml_path)
            XmlBioFM.write_new_parameter_file(
                directory_name, new_parameters, output_file_name)

    @staticmethod
    def _xml_to_dict(element: ET.Element) -> Dict[str, Any]:
        """
        Convert an XML element to a dictionary.

        Args:
            element (ET.Element): XML element.

        Returns:
            Dict[str, Any]: Dictionary representation.
        """
        result = {
            "_tag": element.tag,
            "_attrib": element.attrib,
            "_children": [XmlBioFM._xml_to_dict(e) for e in element]
        }
        return result

    @staticmethod
    def _dict_to_xml(data: Dict[str, Any]) -> ET.Element:
        """
        Convert a dictionary to an XML element.

        Args:
            data (Dict[str, Any]): Dictionary representation.

        Returns:
            ET.Element: XML element.
        """
        element = ET.Element(data["_tag"], attrib=data["_attrib"])
        for child_data in data["_children"]:
            child = XmlBioFM._dict_to_xml(child_data)
            element.append(child)
        return element