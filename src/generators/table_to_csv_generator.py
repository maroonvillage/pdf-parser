import csv
from datetime import datetime
import json
import logging
import os
import re
from typing import Dict, Any, List

def json_to_csv_table_layout(json_data: Dict[str, Any], output_file_path: str) -> None:
    """
    Parses JSON data representing a table and saves it to a CSV file, attempting to match the visual layout of the table.

    Parameters:
        json_data (Dict[str, Any]): The JSON data representing a table with categories and subcategories.
        output_file_path (str): The path to save the CSV file.
    """
    log = logging.getLogger(__name__)
    try:
        if not json_data:
            log.warning("The json data is empty.")
            return

        title = json_data.get("title", "No Title")
        columns = json_data.get("columns", [])
        rows = json_data.get("rows", [])

        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title]) #Write title first
            writer.writerow(columns) #Write header columns

            if rows:
                current_category = ""
                for row in rows:
                   category = row.get("Categories", "")
                   subcategory = row.get("Subcategories", "")
                   if category:
                        current_category = category
                        writer.writerow([category, subcategory])
                   else:
                        writer.writerow([current_category, subcategory])
         
            
            log.info(f"Successfully wrote json data to csv file: {output_file_path}")
    except FileNotFoundError as e:
         log.error(f"FileNotFoundError: {e} when saving to file: {output_file_path}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e} when saving data to csv. JSON Data: {json_data}. Error: {e}")

def json_to_csv_table_layout2(json_data: List[Dict], output_file_path: str) -> None:
    """
     Parses JSON data representing multiple tables and saves them to a CSV file while trying to match the original visual structure.

    Parameters:
        json_data (List[Dict]): The JSON data containing tables with columns and rows.
       output_file_path (str): The path to save the CSV file.
    """
    log = logging.getLogger(__name__)
    try:
        if not json_data:
            log.warning("The json data is empty.")
            return
        
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for table in json_data:
                  title = table.get("title", "")
                  if not re.match(r"^Table\s+\d+[\s\S]*", title, re.IGNORECASE):
                    log.debug(f'skipping non-table title: {title}')
                    continue #Skips if the title does not match table pattern

                  writer.writerow([title]) # Write the title
                  columns = table.get("columns", []) # Get the columns
                  rows = table.get("rows", []) # Get the rows
                  writer.writerow(columns) #Write header row

                  if rows:
                      for row in rows:
                        row_values = []
                        for col in columns:
                            row_values.append(row.get(col,"")) #Extract column data from the row
                        if not columns:
                            #If there are not columns, then iterate though the row dictionary
                           for value in row.values():
                                 row_values.append(value)
                        writer.writerow(row_values)
                  else:
                    log.warning(f"No data to output for table: {title}")
    
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
    output_file = f"table_json_to_csv_{timestamp}.csv"
    
    
    json_folder = "data/output/parsed"
    full_output_path = os.path.join("data/output/parsed", output_file)
    
    first_file = True
    try:
       
        for filename in os.listdir(json_folder):
            if "json_table_output" in filename and filename.endswith(".json"):
                 json_file_path = os.path.join(json_folder, filename)
                 log.info(f"Processing file: {json_file_path}")
                 json_data = {}
                 try:
                    with open(json_file_path, 'r') as f:
                        json_data = json.load(f)
                        json_to_csv_table_layout2(json_data, full_output_path)
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