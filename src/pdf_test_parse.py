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

from api_caller import call_api, upload_file, call_unstructured
from file_util import *

from sentence_transformers import SentenceTransformer
from data.pinecone_vector_db import PineConeVectorDB
from data.graph_db import GraphDatabase
#from data_util import *

from parse_util import *

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

import re

def find_string(text, string_to_find):
    
    # Define the regex pattern to match the word "Title"
    pattern = fr'\b{string_to_find}\b'
    
    # Use re.search to find the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        return f"Found '{match.group()}' at position {match.start()} to {match.end()}"
    else:
        return "Title not found"




def main():

    print('Hello, world from pdf_test_parse main!')
    
    """     str1 = "AI_Risk_Management-NIST.AI.100-1"
    str2 = "ISO+IEC+23894-2023"
    
    stripped_str1 = strip_non_alphanumeric(str1)
    
    print(stripped_str1)
    
    stripped_str2 = strip_non_alphanumeric(str2)
    
    print(stripped_str2)
    
    
    # Example usage
    sample_text = "Appendix: A: Descriptions of AI Actor Tasks from Figures 2 and 3"
    result = find_string(sample_text, "Appendix: A")
    print(result)


    # Example usage
    sample_text = "Appendix A:"
    cleaned_text = strip_non_alphanumeric_end(sample_text)
    print(cleaned_text) """

    sample_json =  [
            {
            "type": "Header",
            "element_id": "f9419a7997760d57b39c54b560a5e57d",
            "text": "NIST AI 100-1",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Header",
            "element_id": "c3e2735004b91871f0b7fa8844219e75",
            "text": "AI RMF 1.0",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "2f53df576aeab76f25c714a31c9b4bfd",
            "text": "GOVERN is a cross-cutting function that is infused throughout AI risk management and enables the other functions of the process. Aspects of GOVERN, especially those related to compliance or evaluation, should be integrated into each of the other functions. Attention to governance is a continual and intrinsic requirement for effective AI risk management over an AI system’s lifespan and the organization’s hierarchy.",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "b3e86bbc15785f06c6f27704af31655b",
            "text": "Strong governance can drive and enhance internal practices and norms to facilitate orga- nizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leader- ship sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "d43e04a85a16f9ab8b98d920e3a65b4f",
            "text": "After putting in place the structures, systems, processes, and teams described in the GOV- ERN function, organizations should benefit from a purpose-driven culture focused on risk understanding and management. It is incumbent on Framework users to continue to ex- ecute the GOVERN function as knowledge, cultures, and needs or expectations from AI actors evolve over time.",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "2ea9b826d62ec84004cd1c0ed13252a4",
            "text": "Practices related to governing AI risks are described in the NIST AI RMF Playbook. Table 1 lists the GOVERN function’s categories and subcategories.",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "c4eaa234ad901eb1b45ab3b019915de2",
            "text": "Table 1: Categories and subcategories for the GOVERN function.",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Table",
            "element_id": "af1102cf6c45104f8b86f228df9b63cb",
            "text": "Categories Subcategories GOVERN 1: GOVERN 1.1: Legal and regulatory requirements involving AI Policies, processes, are understood, managed, and documented. procedures, and practices across the organization related to the mapping, measuring, and managing of AI risks are in place, GOVERN 1.2: The characteristics of trustworthy AI are inte- grated into organizational policies, processes, procedures, and practices. GOVERN 1.3: Processes, procedures, and practices are in place to determine the needed level of risk management activities based on the organization’s risk tolerance. transparent, and GOVERN 1.4: The risk management process and its outcomes are implemented established through transparent policies, procedures, and other effectively. controls based on organizational risk priorities.",
            "metadata": {
                "text_as_html": "<table><thead><tr><th>Categories</th><th>Subcategories</th></tr></thead><tbody><tr><td>GOVERN 1:</td><td>GOVERN 1.1: Legal and regulatory requirements involving Al</td></tr><tr><td>managing of Al risks are in place,</td><td>to determine the needed level of risk management activities based on the organization’s risk tolerance.</td></tr><tr><td>transparent, and implemented\n effectively.</td><td>GOVERN 1.4: The risk management process and its outcomes are established through transparent policies, procedures, and other controls based on organizational risk priorities.</td></tr></tbody></table>",
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "82133fbe6be3f2df697d96b40878c00b",
            "text": "Continued on next page",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "parent_id": "c3e2735004b91871f0b7fa8844219e75",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "PageNumber",
            "element_id": "3dd984e8964241732778b43f7324ed13",
            "text": "Page 22",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 27,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Header",
            "element_id": "d578ed3de760385975da804c89b63327",
            "text": "NIST AI 100-1",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 28,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Header",
            "element_id": "56279384b2f8fe6311da9635526a27c0",
            "text": "AI RMF 1.0",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 28,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "83a26ab6e9a5bb9ec025cfcc92055d12",
            "text": "Table 1: Categories and subcategories for the GOVERN function. (Continued)",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 28,
                "parent_id": "56279384b2f8fe6311da9635526a27c0",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Table",
            "element_id": "01f12090c2cdb8a847aab7a27319527f",
            "text": "Categories Subcategories GOVERN 1.5: Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and or- ganizational roles and responsibilities clearly defined, including determining the frequency of periodic review. GOVERN 1.6: Mechanisms are in place to inventory AI systems and are resourced according to organizational risk priorities. GOVERN 1.7: Processes and procedures are in place for decom- missioning and phasing out AI systems safely and in a man- ner that does not increase risks or decrease the organization’s trustworthiness. GOVERN 2: GOVERN 2.1: Roles and responsibilities and lines of communi- Accountability cation related to mapping, measuring, and managing AI risks are structures are in documented and are clear to individuals and teams throughout place so that the the organization. appropriate teams and individuals are empowered, responsible, and trained for mapping, measuring, and managing AI risks. GOVERN 2.2: The organization’s personnel and partners receive AI risk management training to enable them to perform their du- ties and responsibilities consistent with related policies, proce- dures, and agreements. GOVERN 2.3: Executive leadership of the organization takes re- sponsibility for decisions about risks associated with AI system development and deployment. GOVERN 3: GOVERN 3.1: Decision-making related to mapping, measuring, Workforce diversity, and managing AI risks throughout the lifecycle is informed by a equity, inclusion, diverse team (e.g., diversity of demographics, disciplines, expe- and accessibility rience, expertise, and backgrounds). processes are prioritized in the mapping, measuring, and GOVERN 3.2: Policies and procedures are in place to define and differentiate roles and responsibilities for human-AI configura- tions and oversight of AI systems. managing of AI risks throughout the lifecycle. GOVERN 4: GOVERN 4.1: Organizational policies and practices are in place Organizational to foster a critical thinking and safety-first mindset in the design, teams are committed development, deployment, and uses of AI systems to minimize to a culture potential negative impacts.",
            "metadata": {
                "text_as_html": "<table><thead><tr><th>Categories</th><th>Subcategories</th></tr></thead><tbody><tr><td></td><td>GOVERN 1.5: Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and or- ganizational roles and responsibilities clearly defined, including determining the frequency of periodic review.</td></tr><tr><td></td><td>GOVERN 1.6: Mechanisms are in place to inventory Al systems and are resourced according to organizational risk priorities.</td></tr><tr><td></td><td>GOVERN 1.7: Processes and procedures are in place for decom- missioning and phasing out Al systems safely and in a man- ner that does not increase risks or decrease the organization’s trustworthiness.</td></tr><tr><td>GOVERN 2: Accountability\n structures are in place so that the</td><td>GOVERN 2.1: Roles and responsibilities and lines of communi- cation related to mapping, measuring, and managing Al risks are documented and are clear to individuals and teams throughout the organization.</td></tr><tr><td rowspan=\"2\">appropriate teams and individuals are empowered,\n responsible, and trained for mapping, measuring, and managing Al risks.</td><td>GOVERN 2.2: The organization’s personnel and partners receive Al risk management training to enable them to perform their du- ties and responsibilities consistent with related policies, proce- dures, and agreements.</td></tr><tr><td>GOVERN 2.3: Executive leadership of the organization takes re- sponsibility for decisions about risks associated with Al system development and deployment.</td></tr><tr><td>GOVERN 3: Workforce diversity, equity, inclusion, and accessibility</td><td>GOVERN 3.1: Decision-making related to mapping, measuring, and managing Al risks throughout the lifecycle is informed by a diverse team (e.g., diversity of demographics, disciplines, expe- rience, expertise, and backgrounds).</td></tr><tr><td>processes are prioritized in the mapping,\n measuring, and managing of Al risks throughout the lifecycle.</td><td>GOVERN 3.2: Policies and procedures are in place to define and differentiate roles and responsibilities for human-Al configura- tions and oversight of Al systems.</td></tr><tr><td>GOVERN 4: Organizational\n teams are committed to a culture</td><td>GOVERN 4.1: Organizational policies and practices are in place to foster a critical thinking and safety-first mindset in the design, development, deployment, and uses of Al systems to minimize potential negative impacts.</td></tr></tbody></table>",
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 28,
                "parent_id": "56279384b2f8fe6311da9635526a27c0",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "4666aaf82956fff651edd42b2c9c0f4e",
            "text": "Continued on next page",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 28,
                "parent_id": "56279384b2f8fe6311da9635526a27c0",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "PageNumber",
            "element_id": "874d456f3659385af127b6720bbbd75b",
            "text": "Page 23",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 28,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Header",
            "element_id": "12db5ca051a089ec8354e8532c9dc9ef",
            "text": "NIST AI 100-1",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Header",
            "element_id": "14b86c3261f8f22dfa3b53eec3852d26",
            "text": "AI RMF 1.0",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "d1b51c4b895c6efda7a394f29ef76f96",
            "text": "Table 1: Categories and subcategories for the GOVERN function. (Continued)",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "parent_id": "14b86c3261f8f22dfa3b53eec3852d26",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Table",
            "element_id": "12e48dd913152b8e8107345b5389db69",
            "text": "Categories Subcategories that considers and GOVERN 4.2: Organizational teams document the risks and po- communicates AI tential impacts of the AI technology they design, develop, deploy, risk. evaluate, and use, and they communicate about the impacts more broadly. GOVERN 4.3: Organizational practices are in place to enable AI testing, identification of incidents, and information sharing. GOVERN 5: GOVERN 5.1: Organizational policies and practices are in place Processes are in to collect, consider, prioritize, and integrate feedback from those place for robust external to the team that developed or deployed the AI system engagement with regarding the potential individual and societal impacts related to relevant AI actors. AI risks. GOVERN 5.2: Mechanisms are established to enable the team that developed or deployed AI systems to regularly incorporate adjudicated feedback from relevant AI actors into system design and implementation. GOVERN 6: Policies GOVERN 6.1: Policies and procedures are in place that address and procedures are AI risks associated with third-party entities, including risks of in- in place to address fringement of a third-party’s intellectual property or other rights. AI risks and benefits arising from third-party software and data and other GOVERN 6.2: Contingency processes are in place to handle failures or incidents in third-party data or AI systems deemed to be high-risk. supply chain issues.",
            "metadata": {
                "text_as_html": "<table><thead><tr><th>Categories</th><th>Subcategories</th></tr></thead><tbody><tr><td>that considers and communicates Al risk</td><td>GOVERN 4.2: Organizational teams document the risks and po- tential impacts of the AI technology they design, develop, deploy, evaluate, and use, and they communicate about the impacts more broadly.\n 4.3: Organizational practices in place enable Al</td></tr><tr><td rowspan=\"2\">GOVERN 5: Processes are in place for robust engagement with relevant AT actors.</td><td>GOVERN 5.1: Organizational policies and practices are in place to collect, consider, prioritize, and integrate feedback from those external to the team that developed or deployed the AI system regarding the potential individual and societal impacts related to Al risks.</td></tr><tr><td>GOVERN 5.2: Mechanisms are established to enable the team that developed or deployed Al systems to regularly incorporate adjudicated feedback from relevant Al actors into system design and and implementation.</td></tr><tr><td>GOVERN 6: Policies and procedures are in place to address</td><td>GOVERN 6.1: Policies and procedures are in place that address Al risks associated with third-party entities, including risks of in- fringement of a third-party’s intellectual property or other rights.</td></tr><tr><td>Al risks and benefits arising from third-party software and data and other supply chain issues.</td><td>GOVERN 6.2: Contingency processes are in place to handle failures or incidents in third-party data or Al systems deemed to be high-risk.</td></tr></tbody></table>",
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "parent_id": "14b86c3261f8f22dfa3b53eec3852d26",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "Title",
            "element_id": "c3a2366f3279d6f9f13a28564cede3d9",
            "text": "5.2 Map",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "parent_id": "14b86c3261f8f22dfa3b53eec3852d26",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "NarrativeText",
            "element_id": "5400f86816779fd118e953a069d0741a",
            "text": "The MAP function establishes the context to frame risks related to an AI system. The AI lifecycle consists of many interdependent activities involving a diverse set of actors (See Figure 3). In practice, AI actors in charge of one part of the process often do not have full visibility or control over other parts and their associated contexts. The interdependencies between these activities, and among the relevant AI actors, can make it difficult to reliably anticipate impacts of AI systems. For example, early decisions in identifying purposes and objectives of an AI system can alter its behavior and capabilities, and the dynamics of de- ployment setting (such as end users or impacted individuals) can shape the impacts of AI system decisions. As a result, the best intentions within one dimension of the AI lifecycle can be undermined via interactions with decisions and conditions in other, later activities.",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "parent_id": "c3a2366f3279d6f9f13a28564cede3d9",
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        },
        {
            "type": "PageNumber",
            "element_id": "60bd0e06bbd597829e2e1fb27a4bc64e",
            "text": "Page 24",
            "metadata": {
                "filetype": "application/pdf",
                "languages": [
                    "eng"
                ],
                "page_number": 29,
                "filename": "AI_Risk_Management-NIST.AI.100-1.pdf"
            }
        }
    ]
    
    loaded_json_data = read_json_file('data/output/downloads/AIRiskManagementNISTAI1001_unstructured_response.json')
    extracted_data = extract_table_data_from_json2(loaded_json_data)
    #print (json.dumps(extracted_data, indent=2))
    save_json_file(extracted_data, 'data/output/downloads/extracted_data_AIRMF.json')
    sys.exit()
    
    # pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    # output_path = 'data/output/AI_Risk_Management-PDFMINER_PARSE_TEST'
    # convert_pdf_to_json(pdf_path, output_path)
    
    # sys.exit()

    # loaded_pdf_json_doc = load_document_from_json('data/output/AI__json_output_2024-12-16_13-53-51.json')
    
    # for section in loaded_pdf_json_doc.sections:
    #     print(section['heading'])

    # sections = get_document_sections('data/output/AI__json_output_2024-12-16_13-53-51.json')
    
    # print(sections)
    
    # embeddings = generate_embeddings(sections)
    
    # print(len(embeddings))
    
        
    #sys.exit()

    # test_files = get_files_from_dir('data/output/downloads',extension='.txt')

    # if(test_files != []):
    #     print(test_files)
    # else:
    #     print('Directory was empty.')

    # #'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    #upload_file("http://localhost:8000/upload", "docs/ISO+IEC+23894-2023.pdf")
    
    #call_unstructured()
    unstructured_json_file = 'data/output/downloads/unstructured_response_AI_RMF.json'
    extract_response = read_json_file(unstructured_json_file)  
    extract_text_from_html(extract_response)
   # html_content = "<table><thead><tr><th></th><th>Principle</th><th>Description (as given in ISO 10 018, Clause 4)</th><th>Implications for the development and use of Al</th></tr></thead><tbody><tr><td>d) d)</td><td>Inclusive Inclusive</td><td>Appropriate and timely involvement of stake- holders enables their knowledge, views and | perceptions to be considered. This results in improved awareness and informed management. in improved awareness and informed risk \n management.</td><td>| Because of the potentially far-reaching im- pacts of Al to stakeholders, it is important |that organizations seek dialog with diverse risk|internal and external groups, both to com- municate harms and benefits, and to incor- porate feedback and awareness into the risk management process. Organizations should also be aware that the use of Al systems can introduce additional stakeholders. The areas in which the knowledge, views and perceptions of stakeholders are of benefit include but are not restricted to: — Machine learning (ML) in particular often relies on the set of data appropriate to fulfil its objectives. Stakeholders can help in the identification of risks regarding the data collection, the processing operations, the source and type of data, and the use of the data for operations, \n situations or where the data subjects can be outliers. The complexity of Al technologies creates challenges related to and transparency explainability of Al systems. The diversity of Al transparency \n further drives these challenges due to characteristics such as multiple types of data modalities, Al model topologies, and transparency and reporting mechanisms that should be selected per stakeholders’ needs. Stakeholders can help to identify the goals and describe the means for enhancing transparency and explainability of Al systems. In certain cases, these goals and means can be generalized across the use case and different stakeholdersinvolved. In other cases, stakeholder segmentation of transparency frameworks and reporting mechanisms can be tailored torelevant personas (e.g. “regulators”, “business owners”, “model risk evaluators”) per the use case. Using Al systems for automated decision-making can directly affect internal and external stakeholders. Such stakeholders can provide their views and perceptions concerning, for example, where human oversight can be needed. Stakeholders can help in defining fairness criteria and also help to identify what constitutes bias porate feedback and awareness into the risk \n management process.\n use of AI systems can introduce additional \n stakeholders.\n the \n risks \n particular  situations  or  where  the \n related \n and \n and \n to \n of \n “business  owners”, \n “model \n risk</td></tr></tbody></table>"
    #html_table_to_json(html_content)

    sys.exit()
    # json_response = call_api("http://localhost:8000/extract2", "uploaded_AI_Risk_Management-NIST.AI.100-1.pdf/24-36/stream")


    # if(json_response.status_code == 200):
    #     data = json_response.json()
    #     print(data)
    #     #Get file name as parameter for next request ...

    #     file_name = data.get("filename")

    #     print(file_name)

    #     json_table_data = call_api("http://localhost:8000/get_tables", file_name)

    #     if(json_table_data.status_code == 200):
    #         print(json_table_data.json())


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

""" def extract_text_from_html(extract_response):
    if(extract_response):
        #TODO: Make call to extract HTML table markup from JSON and persist as JSON in a new file
        tables = []
        for table in extract_response:
            #tables.append(table)
            if(table['type'] == "Table"):
                meta_data = table['metadata']
                title = f'<h1>{table['text']}</h1>'
                html_mark_up = f'{title} {meta_data['text_as_html']}'
                #print(meta_data['text_as_html'])
                tables.append(html_mark_up)
                #print()
        #html_table_to_json(tables)
    table_file_path = 'data/output'
    
    
    count = 1
    for table in tables:
        print(table)
        print()
        file_name = generate_filename(f"extracted_tables_{count}","json")
        full_path = os.path.join(table_file_path, file_name)
        html_table_to_json(table, full_path)
        count += 1 """


    #files =  os.listdir(downloads)
    # Filter the list to include only JSON files 
    #filtered_files = [f for f in files if f.endswith('.json')]
    # Sort the list using the custom sorting function
    #sorted_filenames = sorted(filtered_files, key=alphanum_key)

    #print("Sorted filenames:", sorted_filenames)


    #json_data = collate_output_tables(downloads)


    # sys.exit()
    

    # nlp = spacy.load('en_core_web_sm')


    # match = find_appendix("Appendix A: This is a test.")

    # # Display the match 
    # if match: 
    #     print("Match found:") 
    #     print(match.group()) 
    # else: 
    #     print("No match found.")


    # sys.exit()

    # list_of_things = []

    # list_of_things.append("Hello")
    # list_of_things.append("world")
    # list_of_things.append("this is a test")
    # list_of_things.append("Goodbye")
    # #doc  = nlp(None)

    # my_str = "The day started out like every other day in October."

    # if("October" in my_str):
    #     print("The sentence contained the token.")

    # # Path to your PDF file
    # #pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'

    # pdf_path = 'docs/ISO+IEC+23894-2023.pdf'

    # #detect_tables(pdf_path)

    # #extract_pdf_pages(pdf_path)

    # #extract_toc_test()

    # test_str = """Hello,  world this is a  test!"""
    
    # sentences  = test_str.split(' ')

    # #print(len(sentences))

    # for sentence in sentences:
    #     print(f'-{sentence}-\n')
    #     #print()

    # print(" ".join(sentences[0:]))


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
