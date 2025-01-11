import csv
from datetime import datetime
import json
import logging
import os
from typing import Dict, Any, List, Optional


def json_to_csv_with_max_score(json_data: Dict[str, Any], output_file_path: str, write_header: bool = True) -> None:
    """
    Parses JSON data representing search results and saves the title and the content with the highest score for each section, to a CSV file.

    Args:
        json_data (Dict[str, Any]): The JSON data containing search results.
        output_file_path (str): The path to save the CSV file.
        write_header (bool): A flag that will write the header if set to true.
    """
    log = logging.getLogger(__name__)
    try:
        if not json_data:
            log.warning("The json data is empty.")
            return

        title = json_data.get("title", "No Title")
        sections = json_data.get("sections", [])

        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(["Title", "Content"])
            
            if sections:
                best_content = ""
                max_score = 0
                for section in sections:
                   
                    content = section.get('content',"")
                    score = section.get("score", 0)
                    if score > max_score:
                        max_score = score
                        best_content = content
                
                writer.writerow([title, best_content])
            else:
                log.warning("No sections found in the json data.")
         
        log.info(f"Successfully wrote json data to csv file: {output_file_path}")
    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e} when saving to file: {output_file_path}")
    except Exception as e:
         log.error(f"An unexpected error occurred: {e} when processing data from the JSON: {json_data}. File: {output_file_path}")


if __name__ == '__main__':
    # Example Usage
    log = logging.getLogger(__name__)
    
     # Get the current date and time
    now = datetime.now()
    # Format the date and time as a string (e.g., '2023-04-06_14-30-00')
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Combine the base name, timestamp, and extension to form the file name
    output_file = f"combined_vector_db_search_results_{timestamp}.csv"
    
    
    json_folder = "data/output/query_results"
    full_output_path = os.path.join("data/output/parsed", output_file)
    
    first_file = True
    try:
       
        for filename in os.listdir(json_folder):
            if "query_results" in filename and filename.endswith(".json"):
                 json_file_path = os.path.join(json_folder, filename)
                 log.info(f"Processing file: {json_file_path}")
                 json_data = {}
                 try:
                    with open(json_file_path, 'r') as f:
                        json_data = json.load(f)
                        json_to_csv_with_max_score(json_data, full_output_path, write_header=first_file)
                        first_file = False
                 except FileNotFoundError as e:
                     log.error(f"File not found: {json_file_path}. Error: {e}")
                 except json.JSONDecodeError as e:
                     log.error(f"JSONDecodeError: {e} when loading file: {json_file_path}. Error: {e}")
                 except Exception as e:
                     log.error(f"An unexpected error occurred: {e} when processing file: {json_file_path}. Error: {e}")
    except FileNotFoundError as e:
         log.error(f"FileNotFoundError: {e} when listing files in folder: {json_folder}. Error: {e}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e} when processing files in folder: {json_folder}. Error: {e}")