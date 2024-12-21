import sys
#import pdfplumber
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, \
    LTLine, LTRect, LTFigure, LTImage, LTTextLineVertical, LTTextGroup, LTTextGroupTBRL, LTComponent, LTContainer
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.converter import PDFPageAggregator
from sentence_transformers import SentenceTransformer
from io import StringIO

import os
import re

import spacy
import pdf_parser_logger as log
from matcher_patterns import *
from api_caller import call_api, upload_file

from file_util import *

from document import Document, Section, Figure, Table

from data.pinecone_vector_db import PineConeVectorDB
from data.graph_db import GraphDB



def extract_toc(pdf_path, output_path=''):

    try:
        with open(pdf_path, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)

            #Get pages 
            #pages = list(PDFPage.get_pages(fp))
            outlines = document.get_outlines()

            if(output_path != ''):
                with open(output_path, 'w') as file:
                    for (level, title, dest, a, se) in outlines:
                        file.write(f'{title}\n') 
                        #print(f'Level: {level}, Title: {title}, dest: {dest}, a: {a}, se: {se}')
            else:
                raise AttributeError("The path is empty!")
    except AttributeError as e:
        raise

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Initialize PDFParser and PDFDocument
        parser = PDFParser(file)
        document = PDFDocument(parser)

        # If the document is password-protected, raise an error
        if not document.is_extractable:
            raise ValueError("Text extraction is not allowed for this PDF")

        # Create a resource manager to store shared resources
        rsrcmgr = PDFResourceManager()

        # Use StringIO to capture the text
        output_string = StringIO()

        # Set parameters for analysis (e.g., to retain layout)
        laparams = LAParams()

        # Create a TextConverter object to convert PDF pages to text
        device = TextConverter(rsrcmgr, output_string, laparams=laparams)

        # Create a PDFPageInterpreter object to process each page
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Extract text from each page of the document
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

        # Get the extracted text
        text = output_string.getvalue()

        # Cleanup
        device.close()
        output_string.close()

        return text
                            
def find_section(text, matching_groups=False):
    sections_pattern = r"^(?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    section_pattern_with_matching_groups = r"^((?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
    

    if(matching_groups == True):
        return re.match(section_pattern_with_matching_groups, text)
    else:
        return re.match(sections_pattern, text)
    
def find_sections(text, matching_groups=False):
    # Regular expressions for detecting chapters, sections, and figures
    #section_pattern = r"\d+(\.\d*)*\s+[A-Z][\w\s]+"
    #\d+\.{1}(\d*(\.\d+))*\s+[A-Za-z][\w\s\-\(\)\:\,]*
    #sections_pattern = r"(\d+\.{1}(\d*)(\.\d+)*\s+[A-Z][\w\W\s]+)"
    #sections_pattern = r"\d+\.{1}(\d+)*(\.\d+)*\s+[A-Za-z][\w\s\-\(\)\:\,]+"
    #sections_pattern = r"(?:\d+\.{1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\(?:\)\:\,]+"
    sections_pattern = r"^(?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    section_pattern_with_matching_groups = r"^((?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
    sections = []

     # Find sections
    if(matching_groups == True):
        sections = re.findall(section_pattern_with_matching_groups, text)
    else:
        sections = re.findall(sections_pattern, text)

    #for section in sections:
    #    print(section)
    #print(sections)
    return sections

def find_figures(text):
    # Regular expressions for detecting chapters, sections, and figures
    figure_pattern = r"^Figure\s\d+|Fig\.\s\d+"

    # Find chapters, sections, and figures
    figures = re.findall(figure_pattern, text)

    #print(figures)
    return figures

def find_appendicies(text):

     # Regular expressions for detecting chapters, sections, and figures
    #appendix_pattern = r"Appendix\s+[A-Z]\:"
    appendix_pattern = r"Appendix\s+[A-Z]\:|Annex\s+[A-Z]\:?"
    # Find chapters, sections, and figures
    appendicies = re.findall(appendix_pattern, text)
    #print(appendicies)
    return appendicies

def find_appendix(text):

     # Regular expressions for detecting chapters, sections, and figures
    #appendix_pattern = r"Appendix\s+[A-Z]\:"
    appendix_pattern = r"Appendix\s+[A-Z]\:|Annex\s+[A-Z]\:?"

    return re.match(appendix_pattern, text)

def create_toc_dictionary(lines_list):
    
    keys = []
    values = []
    dict = {}
    line_no = 1

    for line in lines_list:
        keys.append(line)
        values.append(line_no)
        line_no += 1

    # Add the list of values to the dictionary
    for key, value_list in zip(keys, values):
        dict[key] = value_list

    return dict

def get_matcher(nlp) -> Matcher:

    matcher = Matcher(nlp.vocab)

    #Add matcher patterns 

    ep_list = get_executive_summary_patterns()

    for pattern in ep_list:
        matcher.add("ExecutiveSummaryMethods", [pattern])

    foreward_list = get_foreward_pattern()

    for pattern in foreward_list:
        matcher.add("ForewardMethods", [pattern])  

    intro_list = get_introduction_pattern()

    for pattern in intro_list:
        matcher.add("IntroMethods", [pattern])  

    summary_list = get_summary_pattern()

    for pattern in summary_list:
        matcher.add("SummaryMethods", [pattern])

    return matcher

def convert_pdf_to_json(pdf_file_path, output_txt_path, output_json_path, lines_list, nlp):

    print('Inside convert_pdf_to_json ... the path is: {pdf_file_path}')

    try:

        #json_ouput_file = 'data/output/ai_rmf_extracted_json.json'
        document_json = Document(output_json_path,[])

        #Initialize JSON document with section headers ...
        for line in lines_list:
             document_json.add_section(Section(line))

        current_section_header = ''
        #Matcher is used to find headings that may not have been captured in the table of contents
        matcher = get_matcher(nlp)

        #Get TOC dictionary ...
        my_dict = create_toc_dictionary(lines_list)

        start_page = 3

        line_count = 0

        if(pdf_file_path != ''):
            with open(output_txt_path, 'w') as wfile:
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
                            #print(f'PageId: {page.pageid}\n')
                            #print(f'Page Number: {page_number}\n')
                            wfile.write(f'PageId: {page.pageid} Page Number: {page_number}\n')
                            wfile.write(f'This dimensions for this page are: {layout.height} height, {layout.width} width\n')
                            # Parse each page layout for structured data like tables here
                            for element in layout:
                                first_line = '' #[]
                                if isinstance(element, LTTextBoxHorizontal):
                             
                                    textbox_content = element.get_text().lstrip().rstrip()
                                    
                                    if(textbox_content != ''):
                                        content_lines_list = textbox_content.split('\n')
                                        first_line = content_lines_list[0]
                                        line_count = len(content_lines_list)

                                    x0, y0, x1, y1 = element.bbox
                                    width = x1 - x0
                                    height = y1 - y0
                                    #wfile.write(f"TextBox: {element.get_text()} -> ({element.x0} ,{element.y0}) ({element.x1} ,{element.y1}) - {element.bbox}\n")
                                    wfile.write(f"TextBox Content: {textbox_content}\n")

                                    #A text box will be a section header alone, a section header followed by a paragraph 
                                    # (typically, the first paragraph just after the section header), or a paragraph alone.
                                    # The same applies to a Fig. caption

                                    #Each time a text box is encountered, examine the content.
                                    #Check for the possibilities listed above ...
                                    #If a section heading is found append a new section with the corresponding header name 
                                    #  Remove the heading and append the paragraph to the list of paragraphs
                                    #Once the 'current heading' variable is set, you will check it upon encountering each text box
                                    #If the 'current heading' variable is empty, this means it is the first section heading 
                                    #encountered.
                                    #If the 'current heading' variable differs from the one found upon a dictionary lookup
                                    #this means that a new section heading has been reached and a new section must be added to the JSON document.

                                    #You will also look for Figure/Fig. followed by a caption which will be in the Textbox content.
                                    #Since a Figure/Fig will be part of a section, it should always be true that the 'current heading' variable
                                    #will contain a value before you encounter a Figure/Fig.  
                                    #print(f'############# First Line: {first_line}#######################\n')
                                    doc  = nlp(first_line)
                                    matches = matcher(doc)
                                    found_sections = find_sections(first_line)

                                    if(matches or found_sections != []):
                                        current_section_header = first_line
                                        wfile.write(f"Found section(s): {current_section_header} ... count {len(found_sections)} \n")
                                        section_match = None
                                        section_match = find_section(current_section_header,matching_groups=True)
                                        if (section_match != None):
                                            wfile.write(f"Section Match found: {section_match}\n")
                                            if(section_match.group(2) != None):
                                                group_match = section_match.group(2)
                                                current_section_header = f'{section_match.group(1).strip()} {section_match.group(2).strip()}'
                                                wfile.write(f'Group 1: -{section_match.group(1)}-')
                                                wfile.write(f'Group 2: -{group_match.lstrip().rstrip()}-')
                                                current_section = document_json.find_section_by_heading(group_match.lstrip().rstrip())
                                                #split textbox content to see if there is more than one element'
                                                if(current_section != None):
                                                    wfile.write(f'Found section object: {current_section}')
                                                    current_section.heading = current_section_header
                                            else:
                                                 wfile.write(f"Group 2 NOT found.\n")
                                        else:
                                            current_section = document_json.find_section_by_heading(current_section_header)

                                        if(line_count > 1):
                                            #Add header to new section
                                            if(current_section != None):
                                                current_section.add_paragraph("\n".join(content_lines_list[1:]))
                                        #else:
                                            #Add header to new section and append first paragraph
                                        #    wfile.write(f"The section was NOT the only textbox content : {textbox_content} line count {line_count} \n")
                                        line_count = 0
                                    elif(find_appendicies(first_line) != []):
                                        
                                        wfile.write(f"Found appendix {textbox_content}\n")
                                        next_line = ''
                                        wfile.write(f"Appendix pattern {find_appendix(first_line).group()}\n")
                                        pattern_match = find_appendix(first_line).group()
                                        if(pattern_match ==  first_line):
                                            wfile.write(f"re match is equal to first line: {find_appendix(first_line).group()} {first_line}\n")
                                            #Capture second line of textbox content and concatenate to end of first line
                                            if(line_count > 1):
                                                next_line = content_lines_list[1]
                                                first_line = f'{first_line} {next_line.lstrip().rstrip()}'

                                        current_section_header= first_line
                                        wfile.write(f"appendix wrapped across 2 lines: {next_line}\n")
                                        current_section = document_json.find_section_by_heading(current_section_header)

                                        if(current_section != None):
                                            current_section.add_paragraph("\n".join(content_lines_list[1:]))

                                    elif(find_figures(first_line) != []):
                                         
                                         wfile.write(f"Found figure {textbox_content}\n")
                                         if(current_section != None):

                                            current_section.add_figure(Figure(textbox_content))
                                    else:
                                        if(current_section_header != ''):
                                            #print(f'The current section is: {current_section_header}')
                                            
                                            current_section = document_json.find_section_by_heading(current_section_header)
                                            if(current_section != None):
                                                current_section.add_paragraph(textbox_content)

                                    

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
                        #print("The document is encrypted and cannot be parsed.")
                        log.logger.warning(f"The document {pdf_file_path} is encrypted and cannot be pasred.")

            save_to_json_file(document_json.to_json(), output_json_path)
        else:
            raise AttributeError("The path is empty!")
    except FileNotFoundError as e: # Code to handle the exception 
        log.logger.error(f"convert_pdf_to_json - {e}")
        raise
    except AttributeError as e:
        raise

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


def main():

    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    base_url = 'http://localhost:8000/'

    input_folder = 'docs'
    output_folder = 'data/output'

    pdf_file_name =  'ISO+IEC+23894-2023.pdf' #'AI_Risk_Management-NIST.AI.100-1.pdf'
    
    pdf_prefix = pdf_file_name[:3]

    # Path to your PDF file
    pdf_path =  os.path.join(input_folder, pdf_file_name)

    parsed_pdf_txt_file_name = generate_filename(f'{pdf_prefix}_extracted')
    parsed_pdf_txt_path = os.path.join(output_folder, parsed_pdf_txt_file_name)

    pdfminer_txt_file_name = generate_filename(f'{pdf_prefix}_pdfminer_extract')
    pdfminer_txt_path = os.path.join(output_folder, pdfminer_txt_file_name)

    toc_ouput_file_name = generate_filename(f'{pdf_prefix}_TOC')
    toc_output_path = os.path.join(output_folder, toc_ouput_file_name)

    json_ouput_file_name = generate_filename(f'{pdf_prefix}_json_output',extension="json")
    json_output_path = os.path.join(output_folder, json_ouput_file_name)

    json_table_output_file_name = generate_filename(f'{pdf_prefix}_json_table_output',extension="json")
    json_table_output_path = os.path.join(output_folder, json_table_output_file_name)

    #TODO: Add logging here ...
    
    log.logger.info(f'File will contain text parsed using Py: {parsed_pdf_txt_path}')
    log.logger.info(f'File will contain text parsed using PDFMiner: {pdfminer_txt_path}')
    log.logger.info(f'File will container table of contents from PDF document: {toc_output_path}')
    log.logger.info(f'File will contain parsed text in JSON format: {json_output_path}')

    text = ''

    # Check if the PDF text file exists
    if not os.path.exists(parsed_pdf_txt_path):
        #print(f'The file {parsed_pdf_txt_path} does NOT exists.')
        log.logger.warning(f'The file {parsed_pdf_txt_path} does NOT exists.')
        #Extract text from PDF ...
        text = extract_text_from_pdf(pdf_path)
        save_file(parsed_pdf_txt_path, text)
    else:
        #print(f'The file {parsed_pdf_txt_path} exists.') 
        log.logger.info(f'The file {parsed_pdf_txt_path} exists.') 

    try:
        
        if (1==0):        
            #Upload PDF file to container running Camelot
            upload_file(f"{base_url}upload", pdf_path)

            log.logger.info(f'main - {pdf_path} successfully uploaded to container.')
            
            #Extract Table of Contents ...
            extract_toc(pdf_path, toc_output_path)
            #TODO: Add log entry 
            #Capture list of lines from Table of Contents
            lines_list = read_lines_into_list(toc_output_path)
            
            log.logger.info(f'main - table for contents of document {pdf_path} sucessfully extracted.')
            
            convert_pdf_to_json(pdf_path,pdfminer_txt_path,json_output_path,lines_list,nlp)
            
            log.logger.info(f'main - pdf text has been sucessfully converted to JSON {json_output_path}.')
            
        
        #TEMPORARY ...
        
        
        #TODO: Automate process to determine the range of pages and the lattice or stream parameters of the API call ...
        extract_response = call_api(f"{base_url}/extract2", f"uploaded_{pdf_file_name}/all/lattice")

        log.logger.info(f"A request to the API has been made. URL: {base_url}/extract2, PARAMS: {pdf_file_name}/all/lattice")
        
        #Get file name of collated table data
        if(extract_response.status_code == 200):
            data = extract_response.json()
            #Get file name as parameter for next request ...
            file_name = data.get("filename")   

            json_table_data = call_api(f"{base_url}get_tables", file_name)

            if(json_table_data.status_code == 200):
                print(json_table_data.json())

            save_json_file(json_table_data.json(), json_table_output_path)  

        #TODO: Convert resultant JSON to correct JSON format
        #SKIP for now ... perform this step when converting JSON to CSV 
        
        sys.exit()
        #TEMPORARY: 
        #json_output_path =  'data/output/AI__json_output_2024-12-16_13-53-51.json'
        #TODO: Add converted JSON to main JSON file
        #loaded_pdf_json_doc = load_document_from_json(json_table_output_path)
        loaded_pdf_json_doc = load_document_from_json(json_output_path)
        #print(loaded_pdf_json_doc)

        #Add embeddings to Pinecone
        sections = get_document_sections(json_output_path)
        
        print(len(sections))

        embeddings = generate_embeddings(sections)
        
        print(embeddings)
        
        pinecone_api_key=os.environ.get("PINECONE_API_KEY")
        pinecond_db = PineConeVectorDB(pinecone_api_key,pdf_prefix)
        print(pinecond_db.index_name)
        pinecond_db.add_embeddings_to_pinecone_index(embeddings)
        
        

        #Iterate through nodes of Graph DB to query vector db
        db_name = os.environ.get("NEO4J_DB_NAME")
        uri = os.environ.get("AURORA_URI")
        user_id = os.environ.get("USER_ID")
        auth_key = os.environ.get("NEO4J_AUTH")
        neo4j_graph_db = GraphDB(db_name, uri, user_id, auth_key)
        
        #Get Records from Graph Db query
        records = neo4j_graph_db.get_keyworsds_graphdb()

        # Loop through results and do something with them
        for record in records:
            keyword = record['Keyword']
            results = pinecond_db.get_vectordb_search_results(keyword)
            #print(results)
            #save_file(results, 'data/output/this_is_a_test.txt')
            pinecond_db.output_search_results_to_file(pdf_prefix, keyword, results, sections)


    except Exception as e:
        print(f"An error occurred: {e}")

    
if __name__ == "__main__":
    main() 