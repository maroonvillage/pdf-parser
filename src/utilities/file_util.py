import os
import json
from datetime import datetime
import logging
from logger_config import configure_logger

from typing import Dict, Any
logging.basicConfig(level=logging.INFO)
from document import Document

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
    log = logging.getLogger(__name__)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            if isinstance(text, str):
                file.write(text)
            else:
                file.write(str(text))
            log.info(f"Successfully written data to file: {file_path}")
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
    except PermissionError as e:
        log.error(f"Permission error: {e} when saving to file: {file_path}")
    except Exception as e:
         log.error(f"An unexpected error occurred: {e} when saving to file: {file_path}")


def save_json_file(data, output_file):
    """Save processed data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        #file.write(data)

def generate_filename(base_name, extension="txt"):
    # Get the current date and time
    now = datetime.now()
    # Format the date and time as a string (e.g., '2023-04-06_14-30-00')
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Combine the base name, timestamp, and extension to form the file name
    filename = f"{base_name}_{timestamp}.{extension}"
    return filename


def download_file_from_container(container_name, container_directory, local_directory):

    # Connect to the Docker client
    client = docker.from_env()

    # Name or ID of your Docker container
    #container_name = "your_container_name"

    # Directory in the Docker container containing the JSON files
    #container_directory = "/path/to/json/files"

    # Local directory to save the downloaded JSON files
    #local_directory = "./downloaded_json_files"

    # Create the local directory if it doesn't exist
    os.makedirs(local_directory, exist_ok=True)

    # Get the container
    container = client.containers.get(container_name)

    # List JSON files in the container directory
    json_files = container.exec_run(f"ls {container_directory}").output.decode().splitlines()

    # Download each JSON file
    for json_file in json_files:
        container_path = os.path.join(container_directory, json_file)
        local_path = os.path.join(local_directory, json_file)
        
        # Copy the file from the container to the local directory
        with open(local_path, "wb") as f:
            bits, stat = container.get_archive(container_path)
            for chunk in bits:
                f.write(chunk)

    print("JSON files downloaded successfully!")

def get_files_from_dir(directory,extension='.json'):

    files =  os.listdir(directory)
    # Filter the list to include only JSON files 
    filtered_files = [f for f in files if f.endswith(extension)]

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