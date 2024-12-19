import os
import json
from datetime import datetime
import docker
from document import Document

def check_for_file(file_path):

    if os.path.isfile(file_path):
        return True
    else:
        return False


def read_lines_into_list(file_path):

    my_dict = {}
    keys = []
    values = []
    line_no = 1
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read and print each line one by one
        for line in file:
            #keys.append(line_no)
            stripped_line = line.strip()
            values.append(stripped_line)
            #print(line.strip())  # Use strip() to remove any leading/trailing whitespace
        print('Finished reading the file.')

    #print(values)
    return values


def write_document_loader_docs_to_file(docs, file_path):
    

        # Open a file in write mode
    with open(file_path, 'w') as file:
        for page in docs:
            # Write some text to the file
            file.write(page.page_content)
            file.write("\n")


def save_file(file_path, text):
    # Open a file in write mode
    with open(file_path, 'w') as file:
        # Write some text to the file
        file.write(text)

    print('Text written to file successfully.')


def save_to_json_file(data, output_file):
    """Save processed data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        #json.dump(data, file, ensure_ascii=False, indent=2)
        file.write(data)

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


def read_json_file(file_path):
    """Read from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def output_search_results_to_file(keyword, search_results, sections):
    # Example structure for storing sections and subsections
    document_json = {
        "title": f"Extracted document for keyword {keyword}",
        "sections": []
    }

    if(search_results):
        # Append sections to the JSON object
        for match in search_results['matches']:
            section_id = int(match['id'])
            document_json["sections"].append({
                "section_id": section_id,
                "content": sections[section_id]
            })
    
        # Remove spaces and set all characters to lower case 
        modified_string = keyword.replace(" ", "").lower()
        file_name = f'query_results_{modified_string}.json'
        
        
        # Save the structured data to a JSON file
        with open(os.path.join('data/output', file_name), 'w') as json_file:
            json.dump(document_json, json_file, indent=2)
        
        print(f"{os.path.join('data/output', file_name)} saved to JSON!")
    else:
        print("No search results!")