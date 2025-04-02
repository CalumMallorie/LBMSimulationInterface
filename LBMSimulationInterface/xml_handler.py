# xml_handler.py

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Tuple, Any, List
import logging
import datetime

class XmlBioFM:
    """
    Class to handle reading, updating, and writing XML parameter files.
    """
    
    @staticmethod
    def setup_logger(simulation_dir: str) -> logging.Logger:
        """
        Set up a logger for XML parameter updates.
        
        Args:
            simulation_dir (str): Path to the simulation directory.
            
        Returns:
            logging.Logger: Configured logger.
        """
        # Create logs directory in the simulation directory if it doesn't exist
        logs_dir = os.path.join(simulation_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create a unique logger for this simulation
        logger = logging.getLogger(f"XmlBioFM_{os.path.basename(simulation_dir)}")
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers if any (to avoid duplicate logging)
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
        
        # Create a file handler for detailed logging
        log_filename = os.path.join(logs_dir, f"parameter_updates_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)  # Log everything to file
        
        # Create a formatter with timestamps
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add the handler to the logger
        logger.addHandler(file_handler)
        
        # Create a console handler for summary output only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only show warnings and errors in console
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger

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
            parameter_updates: Dict[str, Any],
            logger: logging.Logger) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Update existing parameters with new values.

        Args:
            parameters (List[Dict[str, Any]]): Existing parameters.
            parameter_updates (Dict[str, Any]): Updates to apply.
            logger (logging.Logger): Logger for recording updates.

        Returns:
            Tuple[List[Dict[str, Any]], int, int]: Updated parameters, count of successful updates, count of failed updates.
        """
        successful_updates = []
        failed_updates = []
        
        for path_str, new_value in parameter_updates.items():
            logger.info(f"Attempting to update parameter: {path_str} = {new_value}")
            
            # Split the path into components
            path_components = path_str.split('.')
            
            found = False
            for element_data in parameters:
                if XmlBioFM.update_parameter(element_data, path_components, new_value, logger):
                    found = True
                    successful_updates.append(path_str)
                    logger.info(f"Successfully updated {path_str} = {new_value}")
                    break
            
            if not found:
                failed_updates.append(path_str)
                logger.warning(f"Failed to find and update {path_str}")
        
        if successful_updates:
            logger.info(f"Successfully updated {len(successful_updates)} parameters: {', '.join(successful_updates)}")
        
        if failed_updates:
            logger.warning(f"Failed to update {len(failed_updates)} parameters: {', '.join(failed_updates)}")
            
        return parameters, len(successful_updates), len(failed_updates)

    @staticmethod
    def update_parameter(element: Dict[str, Any],
                         path_components: List[str],
                         new_value: Any,
                         logger: logging.Logger) -> bool:
        """
        Recursively update the attribute value of an XML element.

        Args:
            element (Dict[str, Any]): XML element as a dictionary.
            path_components (List[str]): Path components split by dots.
            new_value (Any): New value to set.
            logger (logging.Logger): Logger for recording updates.
        
        Returns:
            bool: Whether the update was successful
        """
        if not path_components:
            return False
        
        # The first component is the element tag we're looking for
        current_tag = path_components[0]
        
        if element["_tag"] == current_tag:
            if len(path_components) == 2:
                # Last component is the attribute name
                attr_name = path_components[1]
                element["_attrib"][attr_name] = str(new_value)
                logger.info(f"Updated {'.'.join(path_components)} = {new_value}")
                return True
            else:
                # We need to navigate deeper in the hierarchy
                next_tag = path_components[1]
                for child in element["_children"]:
                    if child["_tag"] == next_tag:
                        # Recursively update the matching child with the remaining path
                        return XmlBioFM.update_parameter(child, path_components[1:], new_value, logger)
                
                # If we reach here, no matching child was found
                logger.warning(f"No child element '{next_tag}' found in '{current_tag}'")
        
        return False

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
    def log_summary(logger: logging.Logger, 
                    total_successful: int, 
                    total_failed: int, 
                    directory_name: str) -> None:
        """
        Log a concise summary of parameter updates.
        
        Args:
            logger (logging.Logger): Logger to use.
            total_successful (int): Number of successfully updated parameters.
            total_failed (int): Number of failed parameter updates.
            directory_name (str): Path to the simulation directory.
        """
        summary = f"Parameter update summary for {os.path.basename(directory_name)}: {total_successful} successful, {total_failed} failed"
        
        # Always show summary in console regardless of log level
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                # Temporarily set level to INFO to ensure summary is shown
                original_level = handler.level
                handler.setLevel(logging.INFO)
                handler.stream.write(f"INFO - {summary}\n")
                handler.stream.flush()
                handler.setLevel(original_level)
        
        # Also log to file
        logger.info(summary)
        
    @staticmethod
    def update_and_write_parameter_files(
            template_path: str,
            directory_name: str,
            parameter_updates_by_file: Dict[str, Dict[Any, Any]]) -> None:
        """
        Update parameter files and write them to the output directory.

        Args:
            template_path (str): Path to the template files.
            directory_name (str): Path to the output directory.
            parameter_updates_by_file (Dict[str, Dict[Any, Any]]): Updates by file.
        """
        # Set up logger for this simulation
        logger = XmlBioFM.setup_logger(directory_name)
        
        full_path_updates = {
            os.path.join(template_path, k): v
            for k, v in parameter_updates_by_file.items()
        }
        logger.info(f"Updating parameter files in {template_path} -> {directory_name}")
        
        total_successful = 0
        total_failed = 0

        for xml_path, parameter_updates in full_path_updates.items():
            logger.info(f"\nProcessing file: {os.path.basename(xml_path)}")
            
            if not os.path.exists(xml_path):
                logger.warning(f"Template file {xml_path} not found")
                continue
                
            parameters = XmlBioFM.read_xml_file(xml_path)
            
            # Ensure parameter paths are in the right format (string paths)
            processed_updates = {}
            for k, v in parameter_updates.items():
                if isinstance(k, tuple):
                    processed_updates['.'.join(k)] = v
                else:
                    processed_updates[k] = v
            
            logger.info(f"Found {len(processed_updates)} parameters to update in {os.path.basename(xml_path)}")
            
            new_parameters, successful, failed = XmlBioFM.calculate_new_parameters(parameters, processed_updates, logger)
            total_successful += successful
            total_failed += failed
            
            output_file_name = os.path.basename(xml_path)
            output_path = os.path.join(directory_name, output_file_name)
            XmlBioFM.write_new_parameter_file(directory_name, new_parameters, output_file_name)
            logger.info(f"Updated parameter file written to {output_path}")
            
        # Log summary info that will appear in console
        XmlBioFM.log_summary(logger, total_successful, total_failed, directory_name)

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

    @staticmethod
    def print_xml_structure(parameters: List[Dict[str, Any]], logger: logging.Logger, indent: int = 0) -> None:
        """
        Log the structure of the XML to help debug path issues.
        
        Args:
            parameters: The XML structure as a list of dictionaries
            logger: Logger to use
            indent: Current indentation level (for recursion)
        """
        for element in parameters:
            logger.debug(" " * indent + f"Element: {element['_tag']}")
            logger.debug(" " * (indent + 2) + f"Attributes: {element['_attrib']}")
            if element['_children']:
                logger.debug(" " * (indent + 2) + "Children:")
                XmlBioFM.print_xml_structure(element['_children'], logger, indent + 4)

    @staticmethod
    def enable_debug_logging(logger: logging.Logger) -> None:
        """
        Enable debug level logging for detailed troubleshooting.
        
        Args:
            logger (logging.Logger): The logger to modify.
        """
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setLevel(logging.DEBUG)
                
        logger.debug("Debug logging enabled")