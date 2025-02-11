import os
import json
from datetime import datetime
import logging
from src.logger_config import configure_logger

from typing import Dict, Any
logging.basicConfig(level=logging.INFO)
from src.document import Document
from typing import List, Dict, Any

def check_for_file(file_path):

    if os.path.isfile(file_path):
        return True
    else:
        return False


def read_lines_into_list(file_path):
    """
    Reads lines from a file and returns them as a list, stripping leading/trailing whitespace.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    list: A list of strings, where each string is a line from the file with whitespace stripped.
    """
    logger = configure_logger(__name__)
    lines = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                lines.append(stripped_line)
            logger.info(f'Finished reading the file {file_path}.')
            return lines
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"An error occurred while reading file: {file_path}. Error: {e}")
        raise


def write_document_loader_docs_to_file(docs, file_path):
    

    # Open a file in write mode
    with open(file_path, 'w') as file:
        for page in docs:
            # Write some text to the file
            file.write(page.page_content)
            file.write("\n")


def save_file(file_path: str, text: Any) -> None:
    """
    Saves a string or other data to a file.

    Parameters:
        file_path (str): The path to the file.
        text (Any): The text or data to write to the file.

    Returns:
        None
    """
    logger = configure_logger(f"{__name__}.save_file")
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            if isinstance(text, str):
                file.write(text)
            else:
                file.write(str(text))
            logger.info(f"Successfully written data to file: {file_path}")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except PermissionError as e:
        logger.error(f"Permission error: {e} when saving to file: {file_path}")
    except Exception as e:
         logger.error(f"An unexpected error occurred: {e} when saving to file: {file_path}")


def save_json_file(data, output_file):
    """Save processed data to a JSON file."""
    with open(output_file, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        #file.write(data)

def write_list_of_table_objects_to_json_file(table_objects: List[Dict[str, Any]], file_path: str) -> None:
    """
    Writes a list of table objects (dictionaries with 'title' and 'rows' keys) to a JSON file.

    Parameters:
        table_objects (List[Dict[str, Any]]): The list of table objects.
        file_path (str): The path to the JSON output file.
    """
    log = logging.getLogger(f'{__name__}.write_list_of_table_objects_to_json_file')
    try:
        if not table_objects:
            log.warning("The table object list is empty. Nothing to write.")
            return
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(table_objects, json_file, indent=4)
        log.info(f"Successfully wrote a list of table objects to file: {file_path}")
    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e} when saving file: {file_path}")
    except TypeError as e:
          log.error(f"TypeError: {e} when processing the table objects. File path: {file_path}. List of table objects {table_objects}")
    except Exception as e:
         log.error(f"An unexpected error occurred: {e} when writing to JSON file: {file_path}. Table Objects: {table_objects}")
         

def write_list_of_table_objects_to_json_file2(table_objects: List[Any], file_path: str) -> None:
    """
    Writes a list of table objects (with a to_dict method) to a JSON file.

    Parameters:
        table_objects (List[Any]): The list of table objects, which may be dictionaries or custom objects.
        file_path (str): The path to the JSON output file.
    """
    log = logging.getLogger(__name__)
    try:
        if not table_objects:
            log.warning("The table object list is empty. Nothing to write.")
            return
        
        serialized_data = []
        for table in table_objects:
            if hasattr(table, 'to_dict'):
                 serialized_data.append(table.to_dict()) # Use to_dict() if available
            elif isinstance(table,dict):
                 serialized_data.append(table) # If it is a dictionary, then just append it to the serialized_data.
            else:
                  log.warning(f'Unsupported object type: {type(table)}')
                  continue
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(serialized_data, json_file, indent=4)
        log.info(f"Successfully wrote a list of table objects to file: {file_path}")
    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e} when saving file: {file_path}")
    except TypeError as e:
          log.error(f"TypeError: {e} when processing the table objects. File path: {file_path}. List of table objects {table_objects}")
    except Exception as e:
         log.error(f"An unexpected error occurred: {e} when writing to JSON file: {file_path}. Table Objects: {table_objects}")


         
def generate_filename(base_name, extension="txt"):
    # Get the current date and time
    now = datetime.now()
    # Format the date and time as a string (e.g., '2023-04-06_14-30-00')
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Combine the base name, timestamp, and extension to form the file name
    filename = f"{base_name}_{timestamp}.{extension}"
    return filename


def get_files_from_dir(directory,extension='.json'):

    files =  os.listdir(directory)
    if(extension!=None):
        # Filter the list to include only files with the specified extension
        filtered_files = [f for f in files if f.endswith(extension)]
    else:
         # Filter the list to include files with any extension
        filtered_files = [f for f in files]

    return filtered_files

def load_document_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return Document.from_dict(data)

def read_json_file(file_path:str) -> Dict[str,Any]:
    """Reads and parses a JSON file, returning its content."""
    import json
    log = logging.getLogger(__name__)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            log.debug(f"Loaded json file: {file_path}")
            return data
    except FileNotFoundError:
         log.error(f"File not found: {file_path}")
         return {}
    except json.JSONDecodeError as e:
         log.error(f"JSONDecodeError: {e} when loading file: {file_path}")
         return {}
    except Exception as e:
        log.error(f"An unexpected error occurred: {e} when processing file: {file_path}")
        return {}