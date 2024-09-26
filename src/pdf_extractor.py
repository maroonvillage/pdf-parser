#import pdfplumber
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from io import StringIO
#import pdfminer.six
#from pdfminer.high_level import extract_text
import os

import re

"""
def open_pdf_file(pdf_path):

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    return text
"""

def extract_toc(pdf_path):
    with open(pdf_path, 'rb') as fp:
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        outlines = document.get_outlines()
        for (level, title, dest, a, se) in outlines:
            print(f'Level: {level}, Title: {title}')
#def extract_tables(text):

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


def find_sections(text):
    # Regular expressions for detecting chapters, sections, and figures
    #section_pattern = r"\d+(\.\d*)*\s+[A-Z][\w\s]+"
    #\d+\.{1}(\d*(\.\d+))*\s+[A-Za-z][\w\s\-\(\)\:\,]*
    #sections_pattern = r"(\d+\.{1}(\d*)(\.\d+)*\s+[A-Z][\w\W\s]+)"
    #sections_pattern = r"\d+\.{1}(\d+)*(\.\d+)*\s+[A-Za-z][\w\s\-\(\)\:\,]+"
    #sections_pattern = r"(?:\d+\.{1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\(?:\)\:\,]+"
    sections_pattern = r"(?:\d+\.{1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
    # Find chapters, sections, and figures
    sections = re.findall(sections_pattern, text)

    print(sections)

def find_figures(text):
    # Regular expressions for detecting chapters, sections, and figures
    figure_pattern = r"Figure\s\d+"

    # Find chapters, sections, and figures
    figures = re.findall(figure_pattern, text)

    print(figures)

def find_tables(text):
    # Regular expressions for detecting chapters, sections, and figures
    table_pattern = r"Table\s\d+"

    # Find chapters, sections, and figures
    tables = re.findall(table_pattern, text)

    print(tables)

def find_appendicies(text):

     # Regular expressions for detecting chapters, sections, and figures
    appendix_pattern = r"Appendix\s+[A-Z]\:"

    # Find chapters, sections, and figures
    appendicies = re.findall(appendix_pattern, text)
    print(appendicies)

def save_file(file_path, text):
    # Open a file in write mode
    with open(file_path, 'w') as file:
        # Write some text to the file
        file.write(text)

    print('Text written to file successfully.')


def main():


    # Path to your PDF file
    pdf_path = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    txt_path = 'docs/extracted_pdf_text.txt'
    print(pdf_path)


    # Check if the file exists
    if not os.path.exists(txt_path):
        print(f'The file {txt_path} does NOT exists.')
        text = extract_text_from_pdf(pdf_path)
        save_file('docs/extracted_pdf_text.txt', text)
    else:
        print(f'The file {txt_path} exists.')

    

    pdf_text = extract_text_from_pdf(pdf_path)

    find_sections(pdf_text)
    find_appendicies(pdf_text)
    find_figures(pdf_text)
    find_tables(pdf_text)


if __name__ == "__main__":
    main() 