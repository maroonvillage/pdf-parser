import requests
from requests import JSONDecodeError
import pdf_parser_logger as log
import json
import os

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
    
    
def call_unstructured():


        url = "https://api.unstructured.io/general/v0/general"
        headers = {
            "accept": "application/json",
            "Content-Type": "multipart/form-data",
            "unstructured-api-key": os.environ.get("UNSTRUCTURED_API_KEY")
        }
        files = {"files": ("document.pdf",open("docs/ISO+IEC+23894-2023.pdf", "rb"))}
        
        response = requests.post(url, headers=headers, files=files)

        # Parse the JSON response
        data = response.json()
        tables = data.get("tables", [])
        for table in tables:
            print(json.dumps(table, indent=4))
