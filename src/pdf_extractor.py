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
from io import StringIO

import os
import re

import spacy
from matcher_patterns import *


from file_util import read_lines_into_list, write_document_loader_docs_to_file, save_file, save_to_json_file, generate_filename

from document import Document, Section, Figure, Table

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

def get_outline_page_no(pages, dest):
        page_num = 0
        # Resolve the destination to get the page object
        dest = resolve1(dest)
        if isinstance(dest, dict) and 'Page' in dest:
            page_obj = dest['Page']
            # Find the corresponding page number
            page_num = next((i + 1 for i, p in enumerate(pages) if p == page_obj), None)
            
            print(f"Page Number: {page_num}")

        return  page_num

def extract_toc(pdf_path, output_path=''):

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
                    print(f'Level: {level}, Title: {title}, dest: {dest}, a: {a}, se: {se}')
        else:
            print('No output path!')
                        
        

def extract_text_from_pdf_lanchain(pdf_path):

    text_pages = extract_text(pdf_path)

    return text_pages


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
    
def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as file:
        parser = PDFParser(file)
        document = PDFDocument(parser)

        if not document.is_extractable:
            raise ValueError("Text extraction is not allowed for this PDF")

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()

        for page_number, page in enumerate(PDFPage.create_pages(document), start=1):
            output_string = StringIO()
            device = TextConverter(rsrcmgr, output_string, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            interpreter.process_page(page)
            text = output_string.getvalue()
            print(f"Page {page_number}:\n{text}")
            device.close()

def find_chapters(text):
    # Regular expressions for detecting chapters, sections, and figures
    chapter_pattern = r"\bChapter\s\d+\b"

    # Find chapters, sections, and figures
    chapters = re.findall(chapter_pattern, text)

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

def find_tables(text):
    # Regular expressions for detecting chapters, sections, and figures
    table_pattern = r"Table\s\d+"

    # Find chapters, sections, and figures
    tables = re.findall(table_pattern, text)

    #print(tables)
    return tables

def find_appendicies(text):

     # Regular expressions for detecting chapters, sections, and figures
    #appendix_pattern = r"Appendix\s+[A-Z]\:"
    appendix_pattern = r"Appendix\s+[A-Z]\:|Annex\s+[A-Z]\:?"
    # Find chapters, sections, and figures
    appendicies = re.findall(appendix_pattern, text)
    #print(appendicies)
    return appendicies

def find_page_number(text):

    page_no_pattern = r"(?:Page|page|pg)\s(?:\d+|[ivx])+"

    # Find chapters, sections, and figures
    page_no = re.findall(page_no_pattern, text)

    return page_no

def is_end_of_sentence(text):
    sentence_endings = ('.', '?', '!', ')')
    return text.endswith(sentence_endings)

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

"""
def extract_tables():

    # Open the PDF file
    with pdfplumber.open("docs/ISO+IEC+23894-2023.pdf") as pdf:
        # Select the first page
        first_page = pdf.pages[7]
        
        # Extract tables
        tables = first_page.extract_table()
        
        if(tables != None):
            # Print the extracted table
            for row in tables:
                print(row)
        else:
            print("No tables were found.")
"""

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

def extract_paragraphs(txt_path, output_file, lines_list, nlp):

    """Parameters: 
    
    txt_path - path to file containing text from pdf document
    output_file - path to the JSON file that will be written 
    lines_list - list of lines from TOC
    nlp - LLM model
    matcher - langchain matcher for some patterns in PDF documents
            """
    my_dict = {}

    section_str = ""
    paragraph = ""
    figure = ""
    found_match = False
    found_section = False
    found_figure = False
    found_table = False
    found_appendix = False
    found_page_no = False
    found_empty_line = False
    is_paragraph_complete = False

    paragraphs = []
    figures = []

    current_section = None
    current_figure = None


    matcher = get_matcher(nlp)

    #Get TOC dictionary ...
    my_dict = create_toc_dictionary(lines_list)

    document_json = Document("ai_rmf_extracted_text_json.json")

    #Open file for writing
    #Open file for reading text from PDF document

    with open(output_file, 'w') as wfile:
        with open(txt_path, 'r') as file:
            # Read and print each line one by one
            for line in file:
                stripped_line = line.lstrip().rstrip() #remove leading and trailing spaces from string while preserving newline characters
                wfile.write(f'stripped line: {stripped_line}\n')
                doc  = nlp(stripped_line)
                matches = matcher(doc)
                if matches:
                    wfile.write(f'MATCHES: {stripped_line}\n')
                    current_section = None
                    section_str = stripped_line
                    current_section = document_json.find_section_by_heading(section_str)
                    if(current_section == None):
                        current_section = Section(section_str)
                        document_json.add_section(current_section)
                        found_match = True
                elif(find_sections(stripped_line) != []):
                    #print(f'Found section: {stripped_line}')
                    current_section = None
                    section_match = None
                    section_match = find_section(stripped_line,matching_groups=True)
                    if (section_match != None):
                        # A section header was found.
                        # Determine that the header is in the dictionary of headers
                        match_str = section_match.group(2)
                        wfile.write(f'{match_str}\n')
                        if(match_str.strip() in my_dict):
                            #Add header to document object
                            section_str = stripped_line
                            wfile.write(f'SECTION {section_str}\n')
                            current_section = document_json.find_section_by_heading(section_str)
                            if(current_section == None):
                                current_section = Section(section_str)
                                document_json.add_section(current_section)
                                found_section = True
                            paragraph = ''
                elif(find_appendicies(stripped_line) != []):
                    current_section = None
                    paragraph = ''
                elif(stripped_line == ''):
                    wfile.write("found empty line\n")
                    #Check for captured paragraph
                    if(paragraph != ''):
                        current_section = document_json.find_section_by_heading(section_str)
                        if(current_section != None):
                            wfile.write("current_section was not None \n")
                            current_section.add_paragraph(paragraph)
                        else:
                            wfile.write("current_section was None \n")
                            current_section = Section(section_str)
                            current_section.add_paragraph(paragraph)
                        wfile.write(f"\tWROTE PARAGRAPH: {section_str} \n")
                        paragraph = ''
                else:
                    wfile.write(f'{stripped_line}\n')
                    paragraph += f'{stripped_line}\n'

    json_ouput_file = 'data/output/ai_rmf_sections_json.json'
    save_to_json_file(document_json.to_json(), json_ouput_file)

def extract_appendicies(txt_path, output_file, lines_list):

    print('Extract Appendicies')

    """Parameters: 
    
    txt_path - path to file containing text from pdf document
    output_file - path to the JSON file that will be written 
    lines_list - list of lines from TOC
    nlp - LLM model
    matcher - langchain matcher for some patterns in PDF documents
            """
    my_dict = {}

    section_str = ""
    paragraph = ""
    figure = ""
    found_match = False
    found_section = False
    found_figure = False
    found_table = False
    found_appendix = False
    found_page_no = False
    found_empty_line = False
    is_paragraph_complete = False

    paragraphs = []
    figures = []

    current_section = None
    current_figure = None

    #Get TOC dictionary ...
    my_dict = create_toc_dictionary(lines_list)

    document_json = Document("ai_rmf_extracted_text_json.json")

    #Open file for writing
    #Open file for reading text from PDF document

    with open(output_file, 'w') as wfile:
        with open(txt_path, 'r') as file:
            # Read and print each line one by one
            for line in file:
                stripped_line = line.lstrip().rstrip() #remove leading and trailing spaces from string while preserving newline characters
                #wfile.write(f'{stripped_line}\n')
                if(find_appendicies(stripped_line) != []):
                    wfile.write(f'APPENDIX: {stripped_line}\n')
                    current_section = None
                    #Check for Appendix section in json document
                    section_str = stripped_line
                    current_section = document_json.find_section_by_heading(section_str)
                    if(current_section == None):
                            current_section = Section(section_str)
                            document_json.add_section(current_section)
                    found_appendix = True
                elif(stripped_line == ''):
                    wfile.write("found empty line\n")
                    #Check for captured paragraph
                    if(paragraph != ''):
                        current_section = document_json.find_section_by_heading(section_str)
                        if(current_section != None):
                            wfile.write("current_section was not None \n")
                            current_section.add_paragraph(paragraph)
                        else:
                            wfile.write("current_section was None \n")
                            current_section = Section(section_str)
                            current_section.add_paragraph(paragraph)
                        wfile.write(f"\tWROTE PARAGRAPH: {section_str} \n")
                        paragraph = ''
                else:
                    wfile.write(f'{stripped_line}\n')
                    paragraph += f'{stripped_line}\n'

    json_ouput_file = 'data/output/ai_rmf_appendicies_json.json'
    save_to_json_file(document_json.to_json(), json_ouput_file)


def extract_figures(txt_path, output_file, lines_list):

    print('Extract Figures')

    """Parameters: 
    txt_path - path to file containing text from pdf document
    output_file - path to the JSON file that will be written 
    lines_list - list of lines from TOC
    """

    my_dict = {}

    section_str = ""
    paragraph = ""
    figure = ""
    found_match = False
    found_section = False
    found_figure = False
    found_table = False
    found_appendix = False
    found_page_no = False
    found_empty_line = False
    is_paragraph_complete = False

    paragraphs = []
    figures = []

    current_section = None
    current_figure = None

    #Get TOC dictionary ...
    my_dict = create_toc_dictionary(lines_list)

    document_json = Document("ai_rmf_extracted_text_figures_json.json")

    #Open file for writing
    #Open file for reading text from PDF document

    with open(output_file, 'w') as wfile:
        with open(txt_path, 'r') as file:
            # Read and print each line one by one
            for line in file:
                stripped_line = line.lstrip().rstrip() #remove leading and trailing spaces from string while preserving newline characters
                #wfile.write(f'{stripped_line}\n')
                if(find_figures(stripped_line) != []):
                    wfile.write(f'FIGURE: {stripped_line}\n')
                    #figure += stripped_line
                    found_figure = True
                elif(stripped_line == ''):
                    wfile.write("found empty line\n")
                    #Check for captured paragraph
                    if(paragraph != ''):
                        current_section = document_json.find_section_by_heading(section_str)
                        if(current_section != None):
                            wfile.write("current_section was not None \n")
                            current_section.add_paragraph(paragraph)
                        else:
                            wfile.write("current_section was None \n")
                            current_section = Section(section_str)
                            current_section.add_paragraph(paragraph)
                        wfile.write(f"\tWROTE PARAGRAPH: {section_str} \n")
                        paragraph = ''
                else:
                    wfile.write(f'{stripped_line}\n')
                    paragraph += f'{stripped_line}\n'

    json_ouput_file = 'data/output/ai_rmf_figures_json.json'
    save_to_json_file(document_json.to_json(), json_ouput_file)


def convert_pdf_to_json(pdf_file_path, output_txt_path, output_json_path, lines_list, nlp):

    print('Inside convert_pdf_to_json ... the path is: {pdf_file_path}')

    try:

        #json_ouput_file = 'data/output/ai_rmf_extracted_json.json'
        document_json = Document(output_json_path)

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
                            print(f'PageId: {page.pageid}\n')
                            print(f'Page Number: {page_number}\n')
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
                                    print(f'############# First Line: {first_line}#######################\n')
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
                                        current_section_header= first_line
                                        current_section = document_json.find_section_by_heading(current_section_header)
                                        if(current_section != None):
                                            current_section.add_paragraph("\n".join(content_lines_list[1:]))

                                    elif(find_figures(first_line) != []):
                                         
                                         wfile.write(f"Found figure {textbox_content}\n")
                                         if(current_section != None):

                                            current_section.add_figure(Figure(textbox_content))
                                    else:
                                        if(current_section_header != ''):
                                            print(f'The current section is: {current_section_header}')
                                            
                                            current_section = document_json.find_section_by_heading(current_section_header)
                                            if(current_section != None):
                                                current_section.add_paragraph(textbox_content)

                                    

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

            save_to_json_file(document_json.to_json(), output_json_path)
        else:
            print('The path is empty!')
    except FileNotFoundError: # Code to handle the exception 
        print("There is no file or the path is incorrect!")

def main():


    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    input_folder = 'docs'
    output_folder = 'data/output'

    #pdf_file_name = 'ISO+IEC+23894-2023.pdf'

    
    pdf_file_name =  'AI_Risk_Management-NIST.AI.100-1.pdf'
    #ISO+IEC+23894-2023
    
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

    print(parsed_pdf_txt_path)
    print(pdfminer_txt_path)
    print(toc_output_path)
    print(json_output_path)


    #sys.exit()

    text = ''

    # Check if the PDF text file exists
    if not os.path.exists(parsed_pdf_txt_path):
        print(f'The file {parsed_pdf_txt_path} does NOT exists.')
        #Extract text from PDF ...
        #docs = extract_text_pypdf(pdf_path)
        text = extract_text_from_pdf(pdf_path)
        save_file(parsed_pdf_txt_path, text)
    else:
        print(f'The file {parsed_pdf_txt_path} exists.')


    #Extract Table of Contents ...
    extract_toc(pdf_path, toc_output_path)
    #extract_toc(pdf_path, '')



    #Capture list of lines from Table of Contents
    lines_list = read_lines_into_list(toc_output_path)
    print(lines_list)
    
    #TODO: Make this call correctly ...
    convert_pdf_to_json(pdf_path,pdfminer_txt_path,json_output_path,lines_list,nlp)

    sys.exit()

    #extract_paragraphs(txt_path, output_file, lines_list, nlp)

    #extract_appendicies(txt_path, 'data/output/parse_pdf_rmf_appendicies_output.txt', lines_list)

    #extract_figures(txt_path, 'data/output/parse_pdf_rmf_figure_output.txt', lines_list)

  

   
    save_to_json_file(document_json.to_json(), json_ouput_file)

    sys.exit()
    ############################################################################

    ############################################################################

    ############################################################################
    
if __name__ == "__main__":
    main() 