import os
import json

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