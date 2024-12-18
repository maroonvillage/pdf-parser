import json
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, \
    LTLine, LTRect, LTFigure, LTImage, LTTextLineVertical, LTTextGroup, LTTextGroupTBRL, LTComponent, LTContainer
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdftypes import resolve1
import spacy
import re
import sys
#from pdfminer.high_level import extract_pages
#from pdfminer.layout import LTTextContainer, LTChar

from api_caller import call_api, upload_file
from file_util import download_file_from_container, generate_filename, save_to_json_file, get_files_from_dir

def parse_appendices(text):
    lines = text.splitlines()
    document = {
        "title": "Document Title",  # You can extract the document title dynamically as needed
        "sections": []
    }

    current_section = None
    inside_appendix = False
    current_paragraph = ""

    for line in lines:
        line = line.strip()

        # Detect the beginning of an appendix section
        if line.lower().startswith("appendix"):
            if current_section:
                # Append any unfinished paragraph to the section
                if current_paragraph:
                    current_section["paragraphs"].append(current_paragraph.strip())
                
                document["sections"].append(current_section)

            # Start a new appendix section
            current_section = {
                "heading": line,
                "paragraphs": [],
                "figures": [],
                "tables": [],
                "pages": []
            }
            current_paragraph = ""
            inside_appendix = True
            continue

        # Detect figure or table references
        elif line.lower().startswith("figure"):
            current_section["figures"].append(line)
        elif line.lower().startswith("table"):
            current_section["tables"].append(line)

        # If we're inside an appendix, gather paragraphs
        elif inside_appendix:
            if line:  # If it's not an empty line, add to the current paragraph
                current_paragraph += " " + line
            else:
                # End of a paragraph, add it to the section
                if current_paragraph:
                    current_section["paragraphs"].append(current_paragraph.strip())
                    current_paragraph = ""

    # Add the last section and paragraph if any
    if current_section:
        if current_paragraph:
            current_section["paragraphs"].append(current_paragraph.strip())
        document["sections"].append(current_section)

    return document


def parse_text_document(text_file_path):

    print('hello world')


def detect_tables(pdf_file_path):

    print(f'Inside detect_tables function ... the path is: {pdf_file_path}')

    try:
        if(pdf_file_path != ''):
            with open('data/output/table_detect_iso_ouput.txt', 'w') as wfile:
                with open(pdf_file_path, 'rb') as file:
                    parser = PDFParser(file)
                    pdf_document = PDFDocument(parser)

                    parser.set_document(pdf_document) #associates the PDF file with the parser
                    if pdf_document.is_extractable:
                        # Set up PDF resources and interpreter
                        resource_manager = PDFResourceManager()
                        laparams = LAParams()
                        device = PDFPageAggregator(resource_manager, laparams=laparams)
                        interpreter = PDFPageInterpreter(resource_manager, device)

                        #for page_number, page in PDFPage.get_pages(file):
                        for page_number, page in enumerate(PDFPage.get_pages(file), start=1):
                            interpreter.process_page(page)
                            layout = device.get_result()  # Layout contains parsed page content
                            print(f'PageId: {page.pageid}\n')
                            print(f'Page Number: {page_number}\n')
                            wfile.write(f'PageId: {page.pageid} Page Number: {page_number}\n')
                            wfile.write(f'This dimensions for this page are: {layout.height} height, {layout.width} width\n')
                            # Parse each page layout for structured data like tables here
                            for element in layout:
                                if isinstance(element, LTTextBoxHorizontal):
                                    
                                    textbox_content = element.get_text()
                                    print("TextBox:", textbox_content)
                                    x0, y0, x1, y1 = element.bbox
                                    width = x1 - x0
                                    height = y1 - y0

                                    content_lines_list = textbox_content.split('\n')
                                    first_line = content_lines_list[0]
                                    line_count = len(content_lines_list)

                                   
                                    wfile.write(f'The first line of the text box is: {first_line}\n')
                                    wfile.write(f'The number of lines in the text box is: {line_count}\n')
                                    
                                    #wfile.write(f"TextBox: {element.get_text()} -> ({element.x0} ,{element.y0}) ({element.x1} ,{element.y1}) - {element.bbox}\n")
                                    wfile.write(f"TextBox Content: {textbox_content}\n")
                                    wfile.write(f"TextBox Position: ({x0}, {y0}), Width: {width}, Height: {height}\n")
                                    print("TextBox Content:", textbox_content)
                                    print(f"TextBox Position: ({x0}, {y0}), Width: {width}, Height: {height}")
                                elif isinstance(element, LTTextLineHorizontal):
                                    print("TextLine:", element.get_text())
                                    wfile.write(f"TextLine: {element.get_text()}\n")
                                elif isinstance(element, LTChar):
                                    print(f"Character: {element.get_text()}, Font: {element.fontname}, Size: {element.size}")
                                    wfile.write(f"Character: {element.get_text()}, Font: {element.fontname}, Size: {element.size}\n")
                                elif isinstance(element, LTLine):
                                    print(f"Line from ({element.x0}, {element.y0}) to ({element.x1}, {element.y1})")
                                    wfile.write(f"Line from ({element.x0}, {element.y0}) to ({element.x1}, {element.y1})\n")
                                elif isinstance(element, LTRect):
                                    print(f"Rectangle with bounding box: ({element.x0}, {element.y0}) - ({element.x1}, {element.y1})")
                                    wfile.write(f"Rectangle with bounding box: ({element.x0}, {element.y0}) - ({element.x1}, {element.y1})\n")
                                elif isinstance(element, LTFigure):
                                    print(f"Figure with width {element.width} and height {element.height}")
                                    wfile.write(f"Figure with width {element.width} and height {element.height}\n")
                                elif isinstance(element, LTImage):
                                    print("Image found with size:", element.srcsize)
                                    wfile.write(f"Image found with size: {element.srcsize} \n")
                                elif isinstance(element, LTTextLineVertical):
                                    print("Vertical line found:", element.get_text())
                                    wfile.write(f"Vertical line found: {element.get_text()} \n")
                                elif isinstance(element, LTTextGroup):
                                    print("Text Group found:", element.get_text())
                                    wfile.write(f"Text Group found: {element.get_text()} \n")
                                elif isinstance(element, LTContainer):
                                    print(f"Found CONTAINER ... {element.bbox}")
                                    wfile.write(f"Found CONTAINER ... {element.bbox}\n")
                                elif isinstance(element, LTTextGroupTBRL):
                                    print(f"Found Text Group TBRL ... {element.bbox}")
                                    wfile.write(f"Found Text Group TBRL ... {element.bbox}\n")

                    else:
                        print("The document is encrypted and cannot be parsed.")

        else:
            print('The path is empty!')
    except FileNotFoundError: # Code to handle the exception 
        print("There is no file or the path is incorrect!")

def extract_pdf_pages(pdf_file_path):

    try:
        for page_layout in extract_pages(pdf_file_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        for character in text_line:
                            if isinstance(character, LTChar):
                                print(character.fontname)
                                print(character.size)

    except FileNotFoundError: # Code to handle the exception 
        print("There is no file or the path is incorrect!")


def extract_toc_test():

    # Open the PDF file
    fp = open('docs/AI_Risk_Management-NIST.AI.100-1.pdf', 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    # Get the outlines
    outlines = document.get_outlines()

    # Process each outline entry
    for level, title, dest, annotation_ref, struct_elem in outlines:
       
        print(f"Title: {title}")
        if struct_elem:
            print(f"Type: {struct_elem.get('Type')}")
            print(f"Role: {struct_elem.get('S')}")
            print(f"Page: {struct_elem.get('Pg')}")
            print(f"ID: {struct_elem.get('ID')}")
            print(f"Attributes: {struct_elem.get('A')}")
            print(f"Children: {struct_elem.get('C')}")
            print(f"MCID: {struct_elem.get('MCID')}")
        if annotation_ref: 
            annotation = resolve1(annotation_ref)
            print(f"Type: {annotation.get('Subtype')}") 
            print(f"Contents: {annotation.get('Contents')}") 
            print(f"Author: {annotation.get('T')}") 
            print(f"CreationDate: {annotation.get('CreationDate')}") 
            print(f"ModificationDate: {annotation.get('M')}") 
            print(f"Color: {annotation.get('C')}") 
            print(f"Flags: {annotation.get('F')}")
        if level:
            print(f'Level: {level}')
        if dest:
            print(f'Destination: {dest}')
        print('-' * 40)

def find_appendix(text):

     # Regular expressions for detecting chapters, sections, and figures
    #appendix_pattern = r"Appendix\s+[A-Z]\:"
    appendix_pattern = r"Appendix\s+[A-Z]\:|Annex\s+[A-Z]\:?"

    return re.match(appendix_pattern, text)

# Custom sorting function
def alphanum_key(filename):
    # Split the filename into parts (prefix and number)
    parts = re.split(r'(\d+)', filename)
    # Convert numeric parts to integers
    return [int(part) if part.isdigit() else part for part in parts]




def collate_output_tables(directory):

    new_json_object = {"tables": []}

    table_index = -1

    table_label_current = ""
    table_name_caption = ""

    table_pattern = r"^\bTable\s\d+\b"

    re_match = None


    # Specify the directory you want to open
    #directory = '.'
    

    files =  os.listdir(directory)
    # Filter the list to include only JSON files 
    filtered_files = [f for f in files if f.endswith('.json')]


    sorted_filenames = sorted(filtered_files, key=alphanum_key)

    # Loop through all the files in the directory 
    # Files are sotred alphanumerically ...
    for filename in sorted_filenames: 
        # Create the full file path 
        file_path = os.path.join(directory, filename) 
        # Check if the file_path is a file (and not a directory) 
        if os.path.isfile(file_path): 
            if filename.endswith(".json"):
                print(file_path)
                with open(file_path, "r") as file:
                    json_data = json.load(file)


                    # Iterate through the list of dictionaries
                    for idx, row in enumerate(json_data):
                        print(row)
                        for key, value in row.items():
                            re_match = re.match(table_pattern, value)
                        
                        if(re_match != None):
                            print(re_match)
                            if(table_label_current != re_match.group(0)):
                                table_label_current = re_match.group(0)
                                table_name_caption = re_match.string
                                new_json_object["tables"].append({"name": table_name_caption, "rows": []})
                                table_index += 1
                        else:
                            if(table_label_current != ''):
                                print(table_label_current)
                                #no match found
                                new_json_object["tables"][table_index]["rows"].append(row)


    """Save processed data to a JSON file."""
    file_name = generate_filename("final_tables","json")
    output_file = f'data/output/{file_name}'
    with open(output_file, 'w') as file:
        json.dump(new_json_object, file, indent=4)
        #file.write(new_json_object)

    return new_json_object


def main():



    print('Hello, world from main!')

    test_files = get_files_from_dir('data/output/downloads',extension='.txt')

    if(test_files != []):
        print(test_files)
    else:
        print('Directory was empty.')

    #'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    upload_file("http://localhost:8000/upload", "docs/AI_Risk_Management-NIST.AI.100-1.pdf")


    json_response = call_api("http://localhost:8000/extract2", "uploaded_AI_Risk_Management-NIST.AI.100-1.pdf/24-36/stream")


    if(json_response.status_code == 200):
        data = json_response.json()
        print(data)
        #Get file name as parameter for next request ...

        file_name = data.get("filename")

        print(file_name)

        json_table_data = call_api("http://localhost:8000/get_tables", file_name)

        if(json_table_data.status_code == 200):
            print(json_table_data.json())


    """Save processed data to a JSON file."""
    #file_name = generate_filename("final_tables","json")
    #output_file = f'data/output/{file_name}'
    #with open(output_file, 'w') as file:
     #   json.dump(json_data, file, indent=4)
    #save_to_json_file(json_data.json(), output_file)
    container_name = 'tenacious-extractor'

    container_path = '/output/parsing'

    local_path = 'data/output/downloads'

    downloads = 'data/output/downloads'


    #files =  os.listdir(downloads)
    # Filter the list to include only JSON files 
    #filtered_files = [f for f in files if f.endswith('.json')]
    # Sort the list using the custom sorting function
    #sorted_filenames = sorted(filtered_files, key=alphanum_key)

    #print("Sorted filenames:", sorted_filenames)


    #json_data = collate_output_tables(downloads)


    sys.exit()
    

    nlp = spacy.load('en_core_web_sm')


    match = find_appendix("Appendix A: This is a test.")

    # Display the match 
    if match: 
        print("Match found:") 
        print(match.group()) 
    else: 
        print("No match found.")


    sys.exit()

    list_of_things = []

    list_of_things.append("Hello")
    list_of_things.append("world")
    list_of_things.append("this is a test")
    list_of_things.append("Goodbye")
    #doc  = nlp(None)

    my_str = "The day started out like every other day in October."

    if("October" in my_str):
        print("The sentence contained the token.")

    # Path to your PDF file
    #pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'

    pdf_path = 'docs/ISO+IEC+23894-2023.pdf'

    #detect_tables(pdf_path)

    #extract_pdf_pages(pdf_path)

    #extract_toc_test()

    test_str = """Hello,  world this is a  test!"""
    
    sentences  = test_str.split(' ')

    #print(len(sentences))

    for sentence in sentences:
        print(f'-{sentence}-\n')
        #print()

    print(" ".join(sentences[0:]))


"""
    # Specify the directory you want to open
    directory = 'data/output'

    files =  os.listdir(directory)
    # Filter the list to include only JSON files 
    sorted_files = [f for f in files if f.endswith('.json')]

    # Sort the list alphanumerically
    sorted_files.sort()

    for filename in sorted_files: 
        print(filename) 

"""


if __name__ == "__main__":
    main() 
