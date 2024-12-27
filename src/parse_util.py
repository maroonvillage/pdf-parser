import json 
from bs4 import BeautifulSoup
from file_util import save_json_file

def html_table_to_json(html_content):
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the title, column names, and row values
    table = soup.find("table")
    title = soup.find("h1").text.strip() if soup.find("h1") else "No Title"
    columns = [th.text.strip() for th in table.find_all("th")]
    rows = [
        {columns[i]: td.text.strip() for i, td in enumerate(tr.find_all("td"))}
        for tr in table.find_all("tr")[1:]  # Skip header row
    ]

    # Convert the extracted data to JSON format
    table_data = {
        "title": title,
        "columns": columns,
        "rows": rows
    }

    # Print or save the JSON data
    print(json.dumps(table_data, indent=4))

    # Optionally, save to a JSON file
    #with open("table_data.json", "w") as f:
    #    json.dump(table_data, f, indent=4)
        
    save_json_file(table_data, 'data/output/iso_table_data.json')
