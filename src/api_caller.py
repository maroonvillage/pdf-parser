import requests
from requests import JSONDecodeError
import logger_config as log
import json
import os
import logging
from typing import Dict, Any

def call_api(base_url, params):

    # Define the base URL of the FastAPI application
    if(base_url == '' or base_url == None):
        base_url = "http://localhost:8000"


    api_url = f"{base_url}/{params}"

     #TODO: Add log entry ...

    response = requests.get(api_url)
    #TODO: Add log entry ...
    # Print the response
    print(response)

    return response


def upload_file(upload_url, pdf_file_path):

    # Define the URL of the FastAPI upload endpoint
    if(upload_url == '' or upload_url == None):
        upload_url = "http://localhost:8000/upload"

    try:
        if(pdf_file_path == '' or pdf_file_path == None):
            raise FileNotFoundError(f'File does not exist or path incorrect: {pdf_file_path}!')
    except FileNotFoundError as e:
        raise


    try:

        files = {"file": open(pdf_file_path, "rb")}
        response = requests.post(upload_url, files=files)

        if(response != None):
            # log the response
            log.logger.info(f'upload_file - Response from API: {response.json()}')

    except JSONDecodeError as e: 
        log.logger.error(f"upload_file - Failed to decode JSON from the response {e}") 
        raise
    except requests.exceptions.RequestException as e: 
        log.logger.error(f"Request failed: {e}")
        raise
    except FileNotFoundError as e:
        log.logger.error(f"upload_file - {e}")
        raise
    
    
def call_unstructured(pdf_path: str) -> Dict[str, Any]:
    """
    Calls the Unstructured API to process a PDF document and returns the API response.

    This function sends a POST request to the Unstructured API with a PDF document and
    returns the API response as a dictionary.

    Parameters:
       pdf_path (str): The path to the PDF file.

    Returns:
        Dict[str, Any]: The JSON response from the API as a dictionary, or an empty dict if an error occurs.
    """
    log = logging.getLogger(__name__)
    url = "https://api.unstructured.io/general/v0/general"

    try:
        api_key = os.environ.get("UNSTRUCTURED_API_KEY")
        if not api_key:
            log.error("Unstructured API key is missing in environment variables.")
            return {}

        headers = {
            "accept": "application/json",
            "unstructured-api-key": api_key,
        }

        with open(pdf_path, "rb") as f:
            files = {"files": ("document.pdf", f)}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            
            data = response.json()

            log.info(f"Successfully called Unstructured API for file: {pdf_path}")
            log.debug(f"API response: {data}")
            return data
    except FileNotFoundError:
        log.error(f"File not found: {pdf_path}")
        return {}
    except requests.exceptions.RequestException as e:
        log.error(f"API request failed: {e}")
        return {}
    except json.JSONDecodeError as e:
         log.error(f"JSON Decode error: {e}")
         return {}
    except Exception as e:
         log.error(f"An unexpected error occurred: {e}")
         return {}
