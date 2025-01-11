import json
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_pages
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

from api_caller import call_api, upload_file, call_unstructured
from src.utilities.file_util import *

from sentence_transformers import SentenceTransformer
from data.pinecone_vector_db import PineConeVectorDB
from data.graph_db import GraphDatabase
#from data_util import *

from src.utilities.parse_util import *

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

def get_document_sections(file_path):

    json_data = read_json_file(file_path)

    sections = []

    heading_title = ''

    for section in json_data['sections']:
        heading_title = section['heading']
        paragraphs = " ".join(section['paragraphs'])
        sections.append(f'{heading_title}\n{paragraphs}')

    return sections

def generate_embeddings(text_chunks, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    # Load a pre-trained model for generating embeddings
    model = SentenceTransformer(model_name)

    # Generate embeddings for each chunk
    section_embeddings = model.encode(text_chunks)
    
    return section_embeddings

def convert_pdf_to_json(pdf_file_path, output_txt_path):

    print(f'Inside convert_pdf_to_json ... the path is: {pdf_file_path}')

    try:

        start_page = 3

        line_count = 0
        
        output_file = generate_filename(output_txt_path)

        if(pdf_file_path != ''):
            with open(output_file, 'w') as wfile:
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

                        # Get the total number of pages in the document 
                        total_pages = len(list(PDFPage.create_pages(pdf_document))) 
                        # Create a set of page numbers from start_page to the last page 
                        page_numbers = set(range(start_page,total_pages))

                        for page_number, page in enumerate(PDFPage.get_pages(file, pagenos=page_numbers)):
                            interpreter.process_page(page)
                            layout = device.get_result()  # Layout contains parsed page content
                            print(f'PageId: {page.pageid}\n')
                            print(f'Page Number: {page_number}\n')
                            wfile.write(f'PageId: {page.pageid} Page Number: {page_number}\n')
                            wfile.write(f'This dimensions for this page are: {layout.height} height, {layout.width} width\n')
                            # Parse each page layout for structured data like tables here
                            for element in layout:
                                first_line = '' #[]
                                if isinstance(element, LTTextBoxHorizontal):

                                    textbox_content = element.get_text().lstrip().rstrip()
                                    x0, y0, x1, y1 = element.bbox
                                    width = x1 - x0
                                    height = y1 - y0
                                    wfile.write(f"TextBox boundaries: {element.get_text()} -> ({element.x0} ,{element.y0}) ({element.x1} ,{element.y1}) - {element.bbox}\n")
                                    #wfile.write(f"TextBox Content: {textbox_content}\n")

                                elif isinstance(element, LTTextLineHorizontal):
                                    #print("TextLine:", element.get_text())
                                    wfile.write(f"TextLine: {element.get_text()}\n")
                                elif isinstance(element, LTChar):
                                    #print(f"Character: {element.get_text()}, Font: {element.fontname}, Size: {element.size}")
                                    wfile.write(f"Character: {element.get_text()}, Font: {element.fontname}, Size: {element.size}\n")
                                elif isinstance(element, LTLine):
                                    #print(f"Line from ({element.x0}, {element.y0}) to ({element.x1}, {element.y1})")
                                    wfile.write(f"Line from ({element.x0}, {element.y0}) to ({element.x1}, {element.y1})\n")
                                elif isinstance(element, LTRect):
                                    #print(f"Rectangle with bounding box: ({element.x0}, {element.y0}) - ({element.x1}, {element.y1})")
                                    wfile.write(f"Rectangle with bounding box: ({element.x0}, {element.y0}) - ({element.x1}, {element.y1})\n")
                                elif isinstance(element, LTFigure):
                                    #print(f"Figure with width {element.width} and height {element.height}")
                                    wfile.write(f"Figure with width {element.width} and height {element.height}\n")
                                elif isinstance(element, LTImage):
                                    #print("Image found with size:", element.srcsize)
                                    wfile.write(f"Image found with size: {element.srcsize} \n")
                                elif isinstance(element, LTTextLineVertical):
                                    #print("Vertical line found:", element.get_text())
                                    wfile.write(f"Vertical line found: {element.get_text()} \n")
                                elif isinstance(element, LTTextGroup):
                                    #print("Text Group found:", element.get_text())
                                    wfile.write(f"Text Group found: {element.get_text()} \n")
                                elif isinstance(element, LTContainer):
                                    #print(f"Found CONTAINER ... {element.bbox}")
                                    wfile.write(f"Found CONTAINER ... {element.bbox}\n")
                                elif isinstance(element, LTTextGroupTBRL):
                                    #print(f"Found Text Group TBRL ... {element.bbox}")
                                    wfile.write(f"Found Text Group TBRL ... {element.bbox}\n")

                    else:
                        print("The document is encrypted and cannot be parsed.")

        else:
            print('The path is empty!')
            
            
        print(f"Finished parsing file: {pdf_file_path}")
    except FileNotFoundError: # Code to handle the exception 
        print("There is no file or the path is incorrect!")

def find_string(text, string_to_find):
    
    # Define the regex pattern to match the word "Title"
    pattern = fr'\b{string_to_find}\b'
    
    # Use re.search to find the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        return f"Found '{match.group()}' at position {match.start()} to {match.end()}"
    else:
        return "Title not found"

def generate_cypher_queries(json_data: List[Dict]) -> List[str]:
    """
        Parses JSON data containing keywords and prompts and generates cypher queries to add the prompt as a property to a node.

        Parameters:
            json_data (List[Dict]): The JSON data containing keywords and prompts.
        Returns:
            List[str]: A list of cypher queries.
    """
    log = logging.getLogger(__name__)
    cypher_queries = []
    try:
        if not json_data:
            log.warning("JSON data is empty")
            return []
        for item in json_data:
            keyword = item.get("keyword")
            prompt = item.get("prompt")
            if keyword and prompt:
                cypher = f"""
                    MATCH (n)
                    WHERE n.name = "{keyword}"
                    SET n.llm_prompt = "{prompt}"
                    RETURN n
                """
                cypher_queries.append(cypher)
                log.debug(f"Generated cypher query for keyword: {keyword}")
            else:
                log.warning(f"Missing keyword or prompt in item: {item}")
        log.info(f"Successfully generated {len(cypher_queries)} cypher queries.")
        return cypher_queries
    except Exception as e:
        log.error(f"An error occurred when generating cypher queries. Error: {e}")
        return []

def extract_textboxes(pdf_path, output_file):
    """Iterates PDF Document and writes textboxes to a file."""
    textboxes = []
    
    with open(output_file, 'w') as wfile:
        for page_layout in extract_pages(pdf_path):
            #print(page_layout.pageid)
            if(page_layout.pageid >= 27 and page_layout.pageid <= 29):
                for element in page_layout:
                    if isinstance(element, LTTextBoxHorizontal):
                        textboxes.append(element)
                        wfile.write(f'Textbox Content: {element.get_text()} \n Bounding box: ({element.x0}, {element.y0}) ({element.x1}, {element.y1})\n')
    
    return textboxes

def extract_textboxes_by_pageid(pdf_path, page_id):
    textboxes = []
    
    for page_layout in extract_pages(pdf_path):
        
        if(page_layout.pageid == page_id):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    textboxes.append(element)
    
    return textboxes

def sort_textboxes(textboxes):
    # Sort by y0 in descending order (top to bottom) and then by x0 in ascending order (left to right)
    #textboxes.sort(key=lambda x: (-x.y0, x.x0))
    textboxes.sort(key=lambda x: (-x.y1))
    return textboxes

def insert_textbox(sorted_textboxes, new_textbox):
    # Find the correct position to insert the new textbox
    for i, textbox in enumerate(sorted_textboxes):
        if (-new_textbox.y0, new_textbox.x0) < (-textbox.y0, textbox.x0):
            sorted_textboxes.insert(i, new_textbox)
            return
    # If not found, append to the end
    sorted_textboxes.append(new_textbox)

def get_unstructured_page_elements(response_json_file) -> str:
    """Extracts page elements like headers, footers, and page numbers from the Unstructured API response.
       Returns a list of dictionaries containing the text and type of each element.
    """
    
    page_element_text = {
        
        "header": "",
        "footer": "",
        "pagenumber": ""
    }
    
    # Read the JSON file
    response_json = read_json_file(response_json_file)
    
    #print(response_json)

    for element in response_json:
        if(element['type'] == 'Header' or element['type'] == 'Footer' or element['type'] == 'PageNumber'):
            if(element['text'] not in page_element_text[element['type'].lower()]):
                page_element_text[element['type'].lower()] += f"{element['text']} "
            
    # Return the elements
    return page_element_text


    
def main():

    print('Hello, world from pdf_test_parse main!')
    
    results = get_unstructured_page_elements('data/output/downloads/api_responses/AIRiskManagementNISTAI1001_unstructured_response.json')
    
    print (results)
    
    
    text ="NIST AI 100-1"
    if(text in results['header']):
        print('This text is in the header')
    elif(text in results['footer']):
        print('This text is in the footer')
    elif(text in results['pagenumber']):
        print('This text is a page number')
    else:
        print('This text is not in the header, footer or page number')

    sys.exit(0)
     # Extract textboxes from the PDF
    textboxes = extract_textboxes('docs/AI_Risk_Management-NIST.AI.100-1.pdf', 'data/output/pdf_output_pdf_test_parse.txt')
    
    
    
    
    #Get Page Ids and Titles for tables from Unstructured API
    extract_response = read_json_file('data/output/downloads/AIRiskManagementNISTAI1001_unstructured_response.json')
    results = get_table_pages_from_json(extract_response)
    pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    all_textboxes = []
    for result in results:
        print(f"{result['page_number']} - {result['title']}")
        print('------------------------------------')
        page_id = result['page_number']
        textboxes = extract_textboxes_by_pageid(pdf_path, page_id)
        all_textboxes.extend(textboxes)
    
    sorted_textboxes = sort_textboxes(all_textboxes)
    print(sorted_textboxes)
    
    sys.exit(0)
    #'docs/ISO+IEC+23894-2023.pdf
    
    
    
    # Sort the textboxes
    #sorted_textboxes = sort_textboxes(textboxes)
    
    # Example: Insert a new textbox (you would get this from further parsing)
    # new_textbox = LTTextBoxHorizontal()
    # new_textbox.x0 = 100
    # new_textbox.y0 = 200
    # new_textbox._objs = [LTTextContainer()]
    # insert_textbox(sorted_textboxes, new_textbox)
    
    # Print the sorted textboxes
    for textbox in textboxes:
        print(f'{textbox.get_text()} -> ({textbox.x0}, {textbox.y0}) ({textbox.x1}, {textbox.y1})')
        
    
    
    #convert_pdf_to_json('docs/AI_Risk_Management-NIST.AI.100-1.pdf', 'data/output/pdf_output_pdf_test_parse.txt')
    #convert_pdf_to_json('docs/ISO+IEC+23894-2023.pdf', 'data/output/ISO_pdf_output_pdf_test_parse.txt')
   
   
    sample_json = [
        {
            "keyword": "AI Ethics",
            "prompt": "What are the guidelines and regulations surrounding the ethical use and development of artificial intelligence?"
        },
        {
            "keyword": "Transparency",
            "prompt": "What are the regulations and guidelines for ensuring transparency in artificial intelligence development, deployment, and decision-making processes?"
        },
        {
           "keyword": "Accountability",
           "prompt": "What are the measures for ensuring transparency and accountability in artificial intelligence decision-making processes?" 
        },
        {
            "keyword": "Bias Mitigation",
            "prompt": "What strategies and techniques are employed to reduce or eliminate biases in artificial intelligence systems to ensure fair and inclusive decision-making processes?" 
         },
        {
            "keyword": "Fairness",
            "prompt": "What are the guidelines and best practices for ensuring transparency, equity, and unbiased decision-making in Artificial Intelligence (AI) systems?"
        },
        {
            "keyword": "Data Privacy",
            "prompt": "What are the regulatory requirements and best practices for ensuring the confidentiality, integrity, and availability of artificial intelligence data in accordance with privacy laws and regulations?"
        },
        {
            "keyword": "Data Protection",
            "prompt": "What are the regulatory guidelines and best practices for ensuring the secure handling and protection of sensitive data in Artificial Intelligence (AI) systems?"
        },
        {
            "keyword": "Regulatory Compliance",
            "prompt": "What are the rules and guidelines for implementing Artificial Intelligence (AI) solutions in a manner that ensures regulatory compliance?"
        },
        {
            "keyword": "GDPR (General Data Protection Regulation)",
            "prompt": "What are the implications of implementing Artificial Intelligence (AI) systems on General Data Protection Regulation (GDPR) compliance in data processing and management?"
        },
        {
            "keyword": "Audit Trails",
            "prompt": "What records and logs are required to maintain transparency and accountability in artificial intelligence systems, ensuring compliance with regulations and industry standards?"
        },
        {
            "keyword": "Explainability",
            "prompt": "What are the best practices and regulations for ensuring transparency and understandability in Artificial Intelligence (AI) decision-making processes?"
        },
        {
            "keyword": "Robustness",
            "prompt": "What steps are taken to ensure the reliability and resilience of artificial intelligence systems in terms of handling edge cases, unexpected inputs, and potential biases?"
        },
        {
            "keyword": "Security",
            "prompt": "What are the measures taken to ensure the confidentiality, integrity, and availability of artificial intelligence systems and data?"
        },
        {
            "keyword": "Human Oversight",
            "prompt": "What role do humans play in ensuring AI systems comply with regulations and standards?"
        },
        {
            "keyword": "Data Governance",
            "prompt": "What are the regulatory frameworks and guidelines for ensuring the responsible use of artificial intelligence (AI) in data handling, storage, and processing?"
        },
        {
            "keyword": "Risk Management",
            "prompt": "What are the best practices and guidelines for ensuring AI systems comply with regulations and mitigate potential risks, and how do organizations implement effective risk management strategies in this area?"
        },
        {
            "keyword": "Ethical AI",
            "prompt": "What are best practices and guidelines for ensuring fairness, transparency, and accountability in the development and deployment of artificial intelligence systems?"
        },
        {
            "keyword": "Algorithmic Accountability",
            "prompt": "What are the guidelines and regulations for ensuring transparency, fairness, and accountability in artificial intelligence (AI) decision-making processes?"
        },
        {
            "keyword": "Model Monitoring",
            "prompt": "What are best practices and strategies for monitoring AI models to ensure regulatory compliance?"
        },
        {
            "keyword": "Compliance Framework",
            "prompt": "What are the guidelines and standards for ensuring artificial intelligence (AI) systems comply with regulatory requirements and industry best practices?"
         },
        {
            "keyword": "Stakeholder Engagement",
            "prompt": "What are best practices for ensuring effective communication and collaboration with various stakeholders, including regulators, customers, employees, and investors, in the development and implementation of artificial intelligence (AI) solutions?"
         },
        {
            "keyword": "Responsible AI",
            "prompt": "What are the guidelines and regulations for ensuring the ethical use and development of artificial intelligence systems?"
        },
        {
            "keyword": "Trustworthiness",
            "prompt": "What are the measures and standards for ensuring the trustworthiness of artificial intelligence systems in various industries?"
        },
         {
            "keyword": "Informed Consent",
            "prompt": "What are the ethical guidelines and regulations for obtaining informed consent from individuals when using artificial intelligence (AI) systems in applications such as healthcare, finance, or education?"
        },
        {
            "keyword": "Impact Assessment",
            "prompt": "What are best practices and guidelines for conducting impact assessments in artificial intelligence (AI) projects to ensure compliance with relevant regulations and standards?"
        },
        {
            "keyword": "Diversity in AI",
            "prompt": "What strategies are being developed and implemented to ensure artificial intelligence (AI) systems are inclusive, unbiased, and reflective of diverse perspectives and experiences?"
        },
        {
            "keyword": "Vendor Compliance",
            "prompt": "What are the guidelines and regulations for ensuring artificial intelligence (AI) vendors comply with industry standards and laws, and how do we ensure their technology meets our organizational requirements?"
        },
        {
            "keyword": "Usage Policies",
            "prompt": "What are the guidelines and regulations governing the usage and application of artificial intelligence (AI) in various industries, organizations, or institutions?"
        },
        {
           "keyword": "Incident Response",
            "prompt": "What are best practices and procedures for responding to and managing artificial intelligence (AI) incidents, ensuring compliance with regulations and industry standards?"
         },
        {
            "keyword": "Regulatory Landscape",
            "prompt": "What are the current regulations and guidelines governing the use of artificial intelligence, and how do they impact an organization's data privacy and security practices?"
        },
        {
            "keyword": "Benchmarking",
            "prompt": "What are the best practices for ensuring artificial intelligence (AI) systems comply with regulations and standards, and how do organizations measure and track their progress in achieving AI compliance?"
        },
        {
             "keyword": "Performance Metrics",
             "prompt": "What are the key indicators used to measure and assess the effectiveness and efficiency of artificial intelligence (AI) systems in complying with regulatory requirements?"
         },
         {
            "keyword": "Adaptive Compliance",
            "prompt": "What are best practices for ensuring artificial intelligence systems comply with changing regulations and industry standards?"
        },
        {
            "keyword": "Data Minimization",
             "prompt": "What are the best practices for minimizing data collection and retention in Artificial Intelligence (AI) systems to ensure compliance with relevant regulations and standards?"
         },
         {
            "keyword": "Cultural Sensitivity",
            "prompt": "What are the best practices for ensuring fairness, equity, and cultural understanding in artificial intelligence (AI) development and deployment?"
        },
         {
            "keyword": "User Rights",
            "prompt": "What are the responsibilities and regulations governing user data privacy and protection in artificial intelligence (AI) systems?"
        },
       {
            "keyword": "Algorithm Bias",
            "prompt": "What are the implications and mitigation strategies for algorithmic bias in artificial intelligence systems on regulatory compliance, data privacy, and fairness in decision-making processes?"
        },
       {
            "keyword": "Training Data Accountability",
             "prompt": "What measures should be taken to ensure accountability and transparency in the use of training data in artificial intelligence systems?"
       },
         {
            "keyword": "Policy Development",
            "prompt": "What are the guidelines and procedures for developing policies that ensure Artificial Intelligence (AI) systems comply with relevant regulations and standards?"
        },
         {
           "keyword": "Legal Liability",
           "prompt": "What are the legal and regulatory implications for organizations using artificial intelligence (AI) in various industries, and how can they mitigate potential legal risks and liabilities?"
        },
        {
            "keyword": "Innovative Regulation",
            "prompt": "What are the latest regulations and guidelines for ensuring the ethical and responsible development, deployment, and maintenance of artificial intelligence systems?"
        }
    ]
    cypher_queries = generate_cypher_queries(sample_json)
    for query in cypher_queries:
        print(query)


if __name__ == "__main__":
    main() 
