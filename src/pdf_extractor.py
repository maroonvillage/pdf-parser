import sys
#import pdfplumber
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from io import StringIO

import os
import re

import spacy
from matcher_patterns import *


from file_util import read_lines_into_list, write_document_loader_docs_to_file, save_file, save_to_json_file

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
    sections_pattern = r"(?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    section_pattern_with_matching_groups = r"((?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
    

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
    sections_pattern = r"(?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    section_pattern_with_matching_groups = r"((?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
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


def convert_pdf_to_json(txt_path, output_file, lines_list, nlp):

    print('Hello, world.')

    #Use PDFDocument, PDFPage, etc. to parse PDF

    #Use layout to get content from PDF document ...

    #All content in PDF document is in TextBoxes

    #Steps to handle content in TextBoxes 

    #1. Look for Headings or Figures or Appendicies or Tables

    #2. Headings
    #   Search for heading string in Textbox
    #   If the heading is by itself -> Add to JSON document under 'heading' key
    #   Continue iterating through textboxes -> Add subsequent paragraphs under the heading until the next heading, figure or table is encountered
    #   If heading is followed by more text --> split the heading out of the textbox content 
    #   Continue iterating through textboxes -> Add subsequent paragraphs under the heading until the next heading, figure or table is encountered 
    #   If Fig is found --> Add to figures under current section.
    #   Check for the position and size of the text box as an indication of the presence of a table
    #   Check for a label (e.g. Table 1, Table A, etc.) and a caption
    #   If a textbox width is a fraction of the width of the page, It is most-likely a textbox in a table
    #   look a the position of the text, it may be the first column from the left or it may be just to the right of the previous column
    

def main():

    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    #figure_list = get_figure_pattern()

    #for pattern in figure_list:
    #    matcher.add("FigureMethods", [pattern])  

    # Path to your PDF file
    pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'

    #pdf_path = 'docs/ISO+IEC+23894-2023.pdf'

    txt_path = 'docs/ai_rmf_extracted_pdf_text2.txt'

    #txt_path = 'docs/iso_iec_extracted_pdf_text2.txt'

    output_file = 'data/output/parse_pdf_rnmf_output.txt'

    #output_file = 'data/output/parse_pdf_iso_output.txt'

    #toc_ouput_file = 'docs/iso_iec_toc.txt'
    toc_ouput_file = 'docs/ai_rmf_toc_test.txt'

    json_ouput_file = 'data/output/ai_rmf_json.json'

    text = ''

    # Check if the PDF text file exists
    if not os.path.exists(txt_path):
        print(f'The file {txt_path} does NOT exists.')
        #Extract text from PDF ...
        #docs = extract_text_pypdf(pdf_path)
        text = extract_text_from_pdf(pdf_path)
        save_file(txt_path, text)
    else:
        print(f'The file {txt_path} exists.')


    #Extract Table of Contents ...
    extract_toc(pdf_path, toc_ouput_file)
    #extract_toc(pdf_path, '')



    #Capture list of lines from Table of Contents
    lines_list = read_lines_into_list(toc_ouput_file)
    print(lines_list)

    sys.exit()

    extract_paragraphs(txt_path, output_file, lines_list, nlp)

    #extract_appendicies(txt_path, 'data/output/parse_pdf_rmf_appendicies_output.txt', lines_list)

    #extract_figures(txt_path, 'data/output/parse_pdf_rmf_figure_output.txt', lines_list)

    sys.exit()

   
    save_to_json_file(document_json.to_json(), json_ouput_file)

    sys.exit()
    ############################################################################

    ############################################################################

    ############################################################################
    
if __name__ == "__main__":
    main() 