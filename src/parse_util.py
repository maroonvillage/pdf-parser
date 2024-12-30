import json 
import logging
import os
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from file_util import save_json_file
from file_util import generate_filename
import re

def extract_html_tables(extract_response: List[Dict], output_dir: str) -> None:
    """
    Extracts HTML table markup from the JSON response, converts it to JSON format,
    and saves it to separate files.

    Parameters:
        extract_response (List[Dict]): The JSON response containing HTML table markup.
        output_dir (str): The directory to save the extracted HTML tables in JSON format.

    Returns:
        None
    """
    log = logging.getLogger(__name__)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        if not extract_response:
            log.warning("The extract response is empty.")
            return
        for index, table_data in enumerate(extract_response):
                metadata = table_data.get("metadata")
                if not metadata:
                   log.warning(f"Metadata not found in table data: {table_data}")
                   continue
                text = table_data.get("text","")
                html_content = metadata.get("text_as_html","")
                if not html_content:
                   log.warning(f"HTML content not found in metadata for table {index}.")
                   continue

                title = f'<h1>{text}</h1>'
                html_mark_up = f'{title} {html_content}'
                file_name = generate_filename(f"extracted_table_{index+1}", "json")
                full_path = os.path.join(output_dir, file_name)
                html_table_to_json(html_mark_up, full_path)
                log.info(f"Saved extracted table to file: {full_path}")

    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e} when saving files. Output directory: {output_dir}")
    except TypeError as e:
        log.error(f"TypeError: {e} when processing response, Response: {extract_response}")
    except KeyError as e:
         log.error(f"KeyError: {e} in response data. Response: {extract_response}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e},  Response: {extract_response}")
        

def html_table_to_json(html_content: str, file_path: str) -> None:
    """
    Parses HTML table content, converts it to JSON, and saves it to a file.

    Parameters:
        html_content (str): The HTML content containing a table.
        file_path (str): The path to save the JSON data.

    Returns:
        None
    """
    log = logging.getLogger(__name__)
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")
        if not table:
            log.warning(f"No table found in HTML content for file: {file_path}")
            json_data = { "html_content": html_content }
            with open(file_path, "w") as file:
                json.dump(json_data, file, indent=4)
            return
        
        title = soup.find("h1").text.strip() if soup.find("h1") else "No Title"
        columns = [th.text.strip() for th in table.find_all("th")]

        rows = []
        for tr in table.find_all("tr")[1:]:  # Skip header row
            tds = tr.find_all("td")
            if len(tds) == len(columns):
                row = {columns[i]: td.text.strip() for i, td in enumerate(tds)}
                rows.append(row)
            else:
                row = {f"Column {i+1}": td.text.strip() for i, td in enumerate(tds)}
                rows.append(row)
            
        table_data = {
            "title": title,
            "columns": columns,
            "rows": rows
        }
        with open(file_path, "w") as file:
            json.dump(table_data, file, indent=4)
        log.debug(f"Saved table data to file: {file_path}")

    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e} when saving to file. File path: {file_path}")
    except AttributeError as e:
       log.error(f"AttributeError: {e} when processing HTML table: {file_path}. HTML Content: {html_content}")
       json_data = { "html_content": html_content }
       with open(file_path, "w") as file:
            json.dump(json_data, file, indent=4)
       log.debug(f"Saved html content to: {file_path}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e} when processing file: {file_path}, HTML content: {html_content}")
        json_data = { "html_content": html_content }
        with open(file_path, "w") as file:
             json.dump(json_data, file, indent=4)
        log.debug(f"Saved html content to: {file_path}")


def strip_non_alphanumeric(input_string):
    """
    Strips all non-alphanumeric characters from the input string.

    Parameters:
        input_string (str): The string to be processed.

    Returns:
        str: The processed string with only alphanumeric characters.
    """
    return re.sub(r'[^a-zA-Z0-9]', '', input_string)


def replace_extra_space(text):
    # Define the regex pattern for the pattern to be replaced
    pattern = r'\s{2,}'
    
    # Use re.sub to replace the multiple spaces with a single space
    result = re.sub(pattern, ' ', text)
    
    return result

def strip_characters(text, patterns):
    """
    Strip specified characters or escape sequences from the text.
    
    Parameters:
    text (str): The input text string.
    patterns (list): A list of regex patterns to be stripped from the text.
    
    Returns:
    str: The cleaned text with specified patterns removed.
    """
    for pattern in patterns:
        text = re.sub(pattern, ' ', text)
    return text

def strip_non_alphanumeric_end(text):
    # Define the regex pattern to match non-alphanumeric characters at the end of the string
    pattern = r'[\W_]+$'
    
    # Use re.sub to replace the matching pattern with an empty string
    result = re.sub(pattern, '', text)
    
    return result



