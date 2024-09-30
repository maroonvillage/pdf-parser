import sys
#import pdfplumber
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from io import StringIO

import os
import re

import spacy
from matcher_patterns import *


from file_util import read_lines_into_list

from document import Document

"""
def open_pdf_file(pdf_path):

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    return text
"""

def extract_toc(pdf_path, output_path=''):
    with open(pdf_path, 'rb') as fp:
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        outlines = document.get_outlines()
        for (level, title, dest, a, se) in outlines:
            print(f'Level: {level}, Title: {title}, dest: {dest}, a: {a}, se: {se}')
        """
        if(output_path != None):
            with open(output_path, 'w') as file:
                for (level, title, dest, a, se) in outlines:
                    file.write(f'{title}\n')
        """

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
    
"""
def parse_pdf_with_miner(path):

    # Extract all text from the PDF file
    text = extract_text(path)

    # Print the extracted text
    print(text)
"""

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
    sections_pattern = r"(?:\d+\.{1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    section_pattern_with_matching_groups = r"((?:\d+\.{1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
    

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
    sections_pattern = r"(?:\d+\.{1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    section_pattern_with_matching_groups = r"((?:\d+\.{1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
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
    figure_pattern = r"Figure\s\d+|Fig\.\s\d+"

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
    appendix_pattern = r"Appendix\s+[A-Z]\:"

    # Find chapters, sections, and figures
    appendicies = re.findall(appendix_pattern, text)
    #print(appendicies)
    return appendicies

def save_file(file_path, text):
    # Open a file in write mode
    with open(file_path, 'w') as file:
        # Write some text to the file
        file.write(text)

    print('Text written to file successfully.')


def is_end_of_sentence(text):
    sentence_endings = ('.', '?', '!')
    return text.endswith(sentence_endings)


def main():

    nlp = spacy.load('en_core_web_sm')
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

    #figure_list = get_figure_pattern()

    #for pattern in figure_list:
    #    matcher.add("FigureMethods", [pattern])  

    # Path to your PDF file
    pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    #pdf_path = 'docs/AI_RMF_Playbook.pdf'
    #pdf_path = 'docs/ISO+IEC+23894-2023.pdf'
    #txt_path = 'docs/ai_rmf_extracted_pdf_text.txt'
    #txt_path = 'docs/ai_playbook_extracted_text.txt'
    #txt_path = 'docs/ai_rmf_toc.txt'
    #txt_path = 'docs/iso_iec_extracted.txt'
    #print(pdf_path)



    # Check if the file exists
    #if not os.path.exists(txt_path):
    #    print(f'The file {txt_path} does NOT exists.')
    #    text = extract_text_from_pdf(pdf_path)
    #    save_file(txt_path, text)
    #else:
    #    print(f'The file {txt_path} exists.')

    #extract_toc(pdf_path, 'docs/iso_iec_toc.txt')

    #pdf_text = extract_text_from_pdf(pdf_path)

    #m = find_section('Executive Summary',matching_groups=True)
    matches = find_sections("1.1 Understanding and Addressing Risks, Impacts, and Harms")
    #find_appendicies(pdf_text)
    #find_figures(pdf_text)
    #find_tables(pdf_text)
    #for section in secs:
    #    print(section) 

    #if(m == 'NoneType'):

    if(matches == []):
        print("none  found")
    else:
        groups = find_section("1.1 Understanding and Addressing Risks, Impacts, and Harms",True)
        print(groups.group(1))
        print(groups.group(2))
        if(groups.groups != None):
            print(f'Match found: {matches}')

    #print('None Type found')
 
    #sys.exit()

    lines_list = read_lines_into_list('docs/ai_rmf_toc.txt')
    print(lines_list)

    my_dict = {}
    keys = []
    values = []
    line_no = 1

    paragraph = None
    figure = None
    found_match = False
    found_section = False
    found_figure = False
    found_table = False
    found_appendix = False
    is_paragraph_complete = False


    paragraphs = []
    figures = []

    for line in lines_list:
        keys.append(line)
        values.append(line_no)
        line_no += 1

    # Add the list of values to the dictionary
    for key, value_list in zip(keys, values):
        my_dict[key] = value_list


    #srch_val = 'Executive Summary'
    #if srch_val in my_dict:
    #   print(f'Found {srch_val} with value.')
    document_json = Document("ai_rmf_extracted_pdf_text.json")


    with open('docs/ai_rmf_extracted_pdf_text.txt', 'r') as file:
        # Read and print each line one by one
        for line in file:
            stripped_line = line.strip()
            doc = nlp(stripped_line)
            matches = matcher(doc)
            if matches:
                print(f'MATCHES: {stripped_line}')
                found_match = True
            if(find_sections(stripped_line) != []):
                #print(f'Found section: {stripped_line}')
                section_match = find_section(stripped_line,matching_groups=True)

                if (section_match != None):
                    #print(f'FOUND: {section_match.group(1)}, {section_match.group(2)}')
                    # A section header was found.
                    # Determine that the 
                    match_str = section_match.group(2)
                    #print(f"Match group 2: '{match_str.strip()}'")
                    if(match_str.strip() in my_dict):
                        print(f'SECTION {stripped_line}\n')
                        found_section = True
            elif(find_figures(stripped_line) != []):
                print(f'FIGURE: {stripped_line}')
                figure += stripped_line
                found_figure = True
            elif(find_tables(stripped_line) != []):
                print(f'TABLE: {stripped_line}')
                found_table =  True
            elif(find_appendicies(stripped_line) != []):
                print(f'APPENDENDIX: {stripped_line}')
                found_appendix = True
            else:
                print("This is a paragraph.")
                if(stripped_line == None):
                    if(found_match or found_section):
                        #Instantiate a section object 
                        print("Found a section heading.")
                    elif(found_table):
                        print("Found a table.")
                    elif(found_appendix):
                        print("Found an appendix.")
                    elif(figure != None and found_figure):
                        print("Add figure text to figure list in JSON.")
                        figures.append(figure)
                        figure = None
                    elif(paragraph != None):
                        if(is_end_of_sentence(stripped_line)):
                            #Add paragraph to the list of paragraphs
                            paragraphs.append(paragraph)
                            paragraph = None
                        else:
                            #Set a flag that indicates that the end of the paragraph has not been reached.
                            is_paragraph_complete = False                  
                else:
                    paragraph += stripped_line

if __name__ == "__main__":
    main() 