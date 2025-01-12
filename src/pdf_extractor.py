import sys
from typing import List, Dict
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, \
    LTLine, LTRect, LTFigure, LTImage, LTTextLineVertical, LTTextGroup, LTTextGroupTBRL, LTCurve, LTContainer
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.converter import PDFPageAggregator
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
import tempfile

import os
import os.path
import numpy as np
import spacy
import logging
from logger_config import configure_logger

from matcher_patterns import *
from api_caller import call_unstructured

from src.utilities.file_util import *
from src.utilities.parse_util import *

from document import Document, Section, Figure, Table

from data.pinecone_vector_db import PineConeVectorDB
from data.graph_db import GraphDB

from processors.element_processors import *

class EmptyPathError(Exception):
    """Exception raised for empty output path."""
    pass

def extract_toc(pdf_path, output_path=''):
    """
    Extracts the table of contents from a PDF file and saves it to an output file.

    Parameters:
    pdf_path (str): The path to the PDF file.
    output_path (str): The path to the output file to store table of content.

    Raises:
    EmptyPathError: If the output path is empty.
    """
    logger = configure_logger("extract_toc")
    if not output_path:
        logger.error("The provided output path is empty.")
        raise EmptyPathError("The provided output path is empty.")
    
    try:
        with open(pdf_path, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)

            # Get pages 
            outlines = document.get_outlines()
            with open(output_path, 'w') as file:
                for (level, title, dest, a, se) in outlines:
                    file.write(f"{title}\n")
            logger.info(f"Successfully extracted table of contents from {pdf_path} and saved to {output_path}")
    except FileNotFoundError:
            logger.error(f"File not found: {pdf_path}")
            raise
    except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
        resource_manager = PDFResourceManager()
    """
    logger = configure_logger("extract_text_from_pdf")
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Initialize PDFParser and PDFDocument
            parser = PDFParser(file)
            document = PDFDocument(parser)

            # Create a resource manager to store shared resources
            rsrcmgr = PDFResourceManager()

            # If the document is password-protected, raise an error
            if not document.is_extractable:
                raise ValueError("Text extraction is not allowed for this PDF")

            # Create a resource manager to store shared resources
            rsrcmgr = PDFResourceManager()

            # Use a temporary file to capture the text
            temp_file = tempfile.TemporaryFile(mode='w+b')

            # Set parameters for analysis (e.g., to retain layout)
            laparams = LAParams()  # Using default values

            # Create a TextConverter object to convert PDF pages to text
            device = TextConverter(rsrcmgr, temp_file, laparams=laparams)

            # Create a PDFPageInterpreter object to process each page
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # Extract text from each page of the document
            pages = list(PDFPage.create_pages(document))
            for page in pages:
                interpreter.process_page(page)

            temp_file.seek(0)
            text = temp_file.read().decode('utf-8')

            return text
    except FileNotFoundError:
         logger.error(f"File not found: {pdf_path}")
         raise # Re-raise the exception to be handled by caller
    except Exception as e:
        logger.error(f"An error occurred during PDF processing: {e}")
        raise #Re-raise to allow caller to catch specific error
    finally:
        # Cleanup
        device.close()
        temp_file.close()
                            
    
def create_toc_dictionary(lines_list: List[str]) -> Dict[str, int]:
    """
    Creates a dictionary from a list of strings, mapping each string to its index + 1 in the list.

    Parameters:
        lines_list (List[str]): A list of strings (table of contents lines).

    Returns:
        Dict[str, int]: A dictionary where keys are the strings and values are the corresponding line numbers.
    """
    log = logging.getLogger(__name__)
    try:
       
        toc_dict = {line: index + 1 for index, line in enumerate(lines_list)}
        log.debug(f"Created toc dictionary: {toc_dict}")
        return toc_dict
    except TypeError as e:
        log.error(f"TypeError occurred: {e}, input is not a list: {lines_list}")
        return {}
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}, input is: {lines_list}")
        return {}

def convert_pdf_to_json(pdf_file_path, output_txt_path, output_json_path, lines_list, nlp, config=None):
    logger = configure_logger("convert_pdf_to_json")
    logger.info(f'Inside convert_pdf_to_json ... the path is: {pdf_file_path}')
    
    if not config:
        config = {
            "section_pattern": r'^(?:\d+\.\s+)(.+)$',
            "section_pattern_with_group": r'^(?:\d+\.\s+)(.+?)(?:\s+-\s+)(.+)?$',
            "appendix_pattern": r'^(Appendix)\s[A-Z]\.(.*)$',
            "figure_pattern": r'^(Figure|Fig\.)\s\d+.*$',
            "patterns_to_strip": [r'\\u20ac', r'\\n', r'€']
        }

    try:
        document_json = Document(output_json_path,[])
        for line in lines_list:
            cleaned_line = strip_characters(line, config["patterns_to_strip"])
            cleaned_line = replace_extra_space(cleaned_line)
            document_json.add_section(Section(cleaned_line.strip()))
        current_section_header = ''
        start_page = 3
        with open(output_txt_path, 'w') as wfile:
            with open(pdf_file_path, 'rb') as file:
                parser = PDFParser(file)
                pdf_document = PDFDocument(parser)
                parser.set_document(pdf_document)
                if pdf_document.is_extractable:
                    resource_manager = PDFResourceManager()
                    laparams = LAParams()
                    device = PDFPageAggregator(resource_manager, laparams=laparams)
                    interpreter = PDFPageInterpreter(resource_manager, device)
                    total_pages = len(list(PDFPage.create_pages(pdf_document)))
                    logger.info(f'Total pages for {pdf_file_path}: {total_pages}')
                    page_numbers = set(range(start_page,total_pages))
                    logger.info(f'Page numbers for {pdf_file_path}: {page_numbers}')
                    for page_number, page in enumerate(PDFPage.get_pages(file, pagenos=page_numbers)):
                        interpreter.process_page(page)
                        layout = device.get_result()
                        wfile.write(f'PageId: {page.pageid} Page Number: {page_number}\n')
                        wfile.write(f'This dimensions for this page are: {layout.height} height, {layout.width} width\n')
                        for element in layout:
                            try:
                                processor = get_element_processor(element, nlp, config)
                                #None
                                current_section_header = processor.process_element(element, document_json, current_section_header, wfile)
                            except ValueError as ve:
                                   logger.warning(f"Unsupported element type: {element}. Error: {ve}")
                            except Exception as e:
                                  logger.error(f"An error occurred while processing layout element. Element: {element}. Error: {e}")
                else:
                    logger.warning(f"The document {pdf_file_path} is encrypted and cannot be parsed.")
                    

        save_file(output_json_path, document_json.to_json())
    except FileNotFoundError as e:
            logger.error(f"convert_pdf_to_json - {e}")
            raise
    except AttributeError as e:
        logger.error(f"AttributeError in convert_pdf_to_json - {e}")
        raise
    except Exception as e:
            logger.error(f"An error occurred during JSON conversion: {e}")
            raise
        
def get_document_sections(file_path: str) -> List[str]:
    """
    Extracts and formats document sections from a JSON file.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        List[str]: A list of formatted document sections.
    """
    logger = configure_logger("get_document_sections")
    try:
        json_data = read_json_file(file_path)
        if not json_data or "sections" not in json_data:
            logger.warning(f"Invalid or missing sections data in JSON file: {file_path}")
            return []

        sections = []
        for section in json_data["sections"]:
            heading = section.get("heading", "")
            paragraphs = " ".join(section.get("paragraphs", []))
            figures = [fig.get("caption", "") for fig in section.get("figures",[])]
            
            sections.append(f"{heading}\n{paragraphs}\n{' '.join(figures)}")
            logger.debug(f"Extracted section: {heading}")
            
        return sections
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except TypeError as e:
         logger.error(f"TypeError: {e} invalid json format {file_path}")
         return []
    except KeyError as e:
         logger.error(f"KeyError: {e} invalid json format {file_path}")
         return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e} when processing file: {file_path}")
        return []

def generate_embeddings(text_chunks: List[str], model_name: str = 'sentence-transformers/all-MiniLM-L6-v2') -> np.ndarray:
    """
    Generates sentence embeddings for a list of text chunks using a SentenceTransformer model.

    Parameters:
        text_chunks (List[str]): A list of text chunks.
        model_name (str): The name or path of the SentenceTransformer model.

    Returns:
        np.ndarray: A numpy array containing the generated embeddings.
    """
    logger = configure_logger("generate_embeddings")
    try:
        logger.info(f"Loading SentenceTransformer model: {model_name}")
        model = SentenceTransformer(model_name)
        logger.debug(f"Successfully loaded SentenceTransformer model: {model_name}")
        section_embeddings = model.encode(text_chunks)
        logger.info(f"Generated embeddings for {len(text_chunks)} text chunks.")
        return section_embeddings
    except Exception as e:
        logger.error(f"An error occurred while generating embeddings using model: {model_name}. Error: {e}")
        return np.array([]) # Return an empty numpy array

        
def main():

    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    base_url = 'http://localhost:8000/'

    input_folder = 'docs'
    output_folder = 'data/output'
    output_folder_parsed = 'data/output/parsed'
    
    pdf_file_name = 'ISO+IEC+23894-2023.pdf' 
    #'AI_Risk_Management-NIST.AI.100-1.pdf'
    #'ISO+IEC+23894-2023.pdf' 
    
    pdf_prefix = pdf_file_name[:3]

    # Path to your PDF file
    pdf_path =  os.path.join(input_folder, pdf_file_name)

    parsed_pdf_txt_file_name = generate_filename(f'{pdf_prefix}_extracted')
    parsed_pdf_txt_path = os.path.join(output_folder_parsed, parsed_pdf_txt_file_name)

    pdfminer_txt_file_name = generate_filename(f'{pdf_prefix}_pdfminer_extract')
    pdfminer_txt_path = os.path.join(output_folder_parsed, pdfminer_txt_file_name)

    toc_ouput_file_name = generate_filename(f'{pdf_prefix}_TOC')
    toc_output_path = os.path.join(output_folder_parsed, toc_ouput_file_name)

    json_ouput_file_name = generate_filename(f'{pdf_prefix}_json_output',extension="json")
    json_output_path = os.path.join(output_folder_parsed, json_ouput_file_name)

    json_table_output_file_name = generate_filename(f'{pdf_prefix}_json_table_output',extension="json")
    json_table_output_path = os.path.join(output_folder_parsed, json_table_output_file_name)

    # Add logging here ...
    # Create a custom logger instance.
    logger = configure_logger(__name__)
    #logger = logging.getLogger(__name__)
    logger.info(f'File will contain text parsed using Py: {parsed_pdf_txt_path}')
    logger.info(f'File will contain text parsed using PDFMiner: {pdfminer_txt_path}')
    logger.info(f'File will container table of contents from PDF document: {toc_output_path}')
    logger.info(f'File will contain parsed text in JSON format: {json_output_path}')

    text = ''

    # Check if the PDF text file exists
    if not os.path.exists(parsed_pdf_txt_path):
        logger.warning(f'The file {parsed_pdf_txt_path} does NOT exists.')
        #Extract text from PDF ...
        text = extract_text_from_pdf(pdf_path)
        save_file(parsed_pdf_txt_path, text)
    else:
        logger.info(f'The file {parsed_pdf_txt_path} exists.') 
        
   
    try:
        
            #Begin by parsing the PDF document 
            
            #Extract Table of Contents ...
            extract_toc(pdf_path, toc_output_path)
            
            #Capture list of lines from Table of Contents 
            lines_list = read_lines_into_list(toc_output_path)
            
            logger.info(f'Table for contents of document {pdf_path} sucessfully extracted.')
            
            convert_pdf_to_json(pdf_path,pdfminer_txt_path,json_output_path,lines_list,nlp)
            
            logger.info(f'PDF text has been sucessfully converted to JSON {json_output_path}.')
            
           

            #Once a call to the Unstructured API is made, the response is saved to a file.  
            # This precludes the need to make repeated calls to the API.
            dowloads_folder = f'{output_folder}/downloads/api_responses'
            modified_pdf_filename = strip_non_alphanumeric(pdf_file_name.replace(".pdf",""))
            unstructured_json_file = os.path.join(dowloads_folder, f'{modified_pdf_filename}_unstructured_response.json')
            if os.path.exists(unstructured_json_file):
                logger.info(f'Unstructured JSON response file exists: {unstructured_json_file}. Reading from file.')
                extract_response = read_json_file(unstructured_json_file)
            else:
                logger.info(f'Unstructured JSON response file does not exist: {unstructured_json_file}. Making call to Unstructured API.')
                extract_response = call_unstructured(pdf_path)
                save_file(unstructured_json_file, json.dumps(extract_response, indent=4))  # Save the response to a file
            
            

            #Extract tables from the response of the Unstructured API and save to JSON file.
            extracted_data = extract_table_data_from_json2(extract_response)
            
            save_json_file(extracted_data, json_table_output_path)

            #loaded_pdf_json_doc = load_document_from_json(json_output_path)

            #Add embeddings to Pinecone
            sections = get_document_sections(json_output_path)
            
            embeddings = generate_embeddings(sections)
                
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
            records = neo4j_graph_db.get_prompts_graphdb()
            
            logger.info(f'Number of records returned from Graph DB: {len(records)}')
            
            print(f"Length of sections: {len(sections)}")

            
            i = 0
            # Loop through results and do something with them
            for record in records:
                llm_prompt = record['Prompt']
                keyword = record['Keyword']

                results = pinecond_db.get_vectordb_search_results(llm_prompt)
                logger.debug(f'Query used on Pinecone: {llm_prompt}')

                keyword = keyword.replace(" ", "_")
                #Save vector search results to file
                file_name = f'{pdf_prefix}_results_vector_{keyword}'
                file_name = generate_filename(file_name, extension='json')
                full_path = os.path.join('data/output/query_results', file_name)
                if results and results.get("matches"):
                    save_file(full_path, results)
                    
                pinecond_db.output_search_results_to_file(pdf_prefix, keyword, results, sections)
                i += 1

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")
    
if __name__ == "__main__":
    main() 