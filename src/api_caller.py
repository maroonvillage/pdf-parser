import requests
from requests import JSONDecodeError

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
        print(e)
        return


    try:

        files = {"file": open(pdf_file_path, "rb")}
        response = requests.post(upload_url, files=files)
        
        #TODO: Add log entry here ...

        if(response != None):
            # Print the response
            print(response.json())

    except JSONDecodeError as e: 
        print(f"Failed to decode JSON from the response {e}") 
    except requests.exceptions.RequestException as e: 
        print("Request failed:",e)
    except FileNotFoundError as e:
        print(e)