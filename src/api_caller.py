import requests
from requests import JSONDecodeError

def call_api(base_url, params):

    # Define the base URL of the FastAPI application
    if(base_url == '' or base_url == None):
        base_url = "http://localhost:8000"

    # Make a GET request to the root endpoint
    #response = requests.get(f"{base_url}/")

    # Print the response
    #print(response.json())

    api_url = f"{base_url}/{params}"

    print(api_url)

    # Make a GET request to the /items/{item_id} endpoint
    item_id = 1
    #response = requests.get(f"{base_url}/items/{item_id}", params={"q": "query string"})
    response = requests.get(api_url)
    # Print the response
    print(response)

    return response


def upload_file(upload_url, pdf_file_path):

    # Define the URL of the FastAPI upload endpoint
    if(upload_url == '' or upload_url == None):
        upload_url = "http://localhost:8000/upload"

    # Path to the PDF file you want to upload
    #pdf_file_path = "path/to/your/document.pdf"

    try:
        if(pdf_file_path == '' or pdf_file_path == None):
            raise FileNotFoundError(f'File does not exist or path incorrect: {pdf_file_path}!')
    except FileNotFoundError as e:
        print(e)
        return


    try:

        files = {"file": open(pdf_file_path, "rb")}
        response = requests.post(upload_url, files=files)

        # Upload the PDF file
        #with open(pdf_file_path, "rb") as file:
            #files = {"file": (file, file, "application/pdf")}
        #    files = {"file": open("example.pdf", "rb")}
        #    response = requests.post(upload_url, files=files)

        if(response != None):
            # Print the response
            print(response.json())

    except JSONDecodeError as e: 
        print(f"Failed to decode JSON from the response {e}") 
    except requests.exceptions.RequestException as e: 
        print("Request failed:",e)
    except FileNotFoundError as e:
        print(e)