import re
from typing import List, Dict, Any
from pdfminer.high_level import extract_pages
from logger_config import configure_logger
from processors.element_processors import *
from document import Table, Row
from utilities.parse_util import find_table_pattern

def textboxes_to_tabular_json(textboxes: List[Dict[str,Any]], header_footer_dict: List[Dict], y_tolerance: float = 10.0) -> List[Table]:
    """
        Parses a list of text boxes ordered by their Y1 value and returns a list of Table objects, with table titles and row data.
         Parameters:
             textboxes (List[Dict[str, Any]]):  A list of textboxes, with x and y coordinates.
             header_footer_dict (List[Dict]): A list of strings with values of headers and footers.
        Returns:
            List[Table]: An list of Table objects
    """
    logger = configure_logger(f"{__name__}.textboxes_to_tabular_json")
    try:
        if not textboxes:
            logger.warning("The textboxes list is empty.")
            return []
        rows = [] #Store all the row values.
        current_row = [] #Store current row of textboxes.
        current_y = None #Store current y value for detecting new rows.
        tables = []
        previous_table_title = None
        current_table = None
        for textbox in textboxes:
            x0, y0, x1, y1 = textbox.bbox
            current_text_box = get_element_processor(textbox)
            #textbox_content = current_text_box.get_text(textbox)
            textbox_content = textbox.get_text()
            
            #Check if it is part of the headßer/footer
            textbox_content = textbox_content.replace("\n","").strip()
            if(textbox_content in header_footer_dict['header'] or textbox_content in header_footer_dict['footer']):
                #logger.debug(f"Textbox contains a header or footer: {textbox_content}")
                continue
            #Check if it is a page number
            if(current_text_box.find_page_number(textbox_content)):
                #logger.debug(f"Textbox contains a page number {textbox_content}")
                continue
            
            #Check for table title/caption
            table_title_match = find_table_pattern(textbox_content)
            if(table_title_match):
                #Check for the string continued ...
                table_title = table_title_match.group(0).strip()
                #logger.info(f"Table title: {table_title}")
                #print(f"Table title found: {table_title}")
                if(not re.search(r'(continued|cont\.{1}?)',table_title.lower(), re.IGNORECASE)):
                    #logger.debug(f'Table title DOES NOT has cont or continued in it: {table_title}')
                    
                    #if(table_title != previous_table_title):
                    if current_table:
                        #Append the current row to previous table, and clear the current row
                        if current_row:
                            sorted_row = sorted(current_row, key=lambda tb: tb.bbox[0])
                            row_data = {}
                            for index, tb in enumerate(sorted_row):
                                row_data[f'Column {index+1}'] = tb.get_text() #get_element_processor(tb).get_text(tb)
                            row = Row(row_data)
                            current_table.add_row(row)
                        current_row = []
                    current_table = Table(table_title)
                    previous_table_title = table_title
                    tables.append(current_table)
                else:
                    #logger.debug(f'Table title HAS cont or continued in it: {table_title}')
                    if current_table and current_row:
                       sorted_row = sorted(current_row, key=lambda tb: tb.bbox[0])
                       row_data = {}
                       for index, tb in enumerate(sorted_row):
                            row_data[f'Column {index+1}'] = tb.get_text() #get_element_processor(tb).get_text(tb)
                       row = Row(row_data)
                       current_table.add_row(row)
                       current_row = []
                
            elif current_y is None:
                #Initialize the first y value.
                current_y = y1
                current_row.append(textbox)
            elif abs(y1 - current_y) <= y_tolerance:
                #If this is on the same row, then add to current row
                current_row.append(textbox)
            else:
                #Not in same row, so process current row, and create new row
                if current_table:
                    sorted_row = sorted(current_row, key=lambda tb: tb.bbox[0])
                    row_data = {}
                    for index, tb in enumerate(sorted_row):
                       row_data[f'Column {index+1}'] = tb.get_text() #get_element_processor(tb).get_text(tb)
                    row = Row(row_data)
                    current_table.add_row(row)
                    current_row = [textbox]
                    current_y = y1 # New y-value.
                else:
                    #This means this textbox is not part of any table
                     current_row = [textbox]
                     current_y = y1
        
        #Process the last row
        if current_table and current_row:
            sorted_row = sorted(current_row, key=lambda tb: tb.bbox[0])
            row_data = {}
            for index, tb in enumerate(sorted_row):
                row_data[f'Column {index+1}'] = tb.get_text() #get_element_processor(tb).get_text(tb)
            row = Row(row_data)
            current_table.add_row(row)

        logger.info(f'Successfully processed list of textboxes.')
        return tables

    except Exception as e:
         logger.error(f"An unexpected error occurred: {e} when processing list of textboxes.")
         return []
     
def get_table_pages_from_unstructured_json(json_data: List[Dict]) -> List[int]:
    """
    Extracts the page numbers of tables from the JSON data.

    Parameters:
        json_data (List[Dict]): The JSON data containing table information.

    Returns:
        List[int]: A list of page numbers where tables are found.
    """
    logger = configure_logger(f"{__name__}.get_table_pages_from_unstructured_json")
    table_data_list = []
    table_titles = {} #Stores all the titles keyed by element_id
    current_table = None
    try:
      if not json_data:
            logger.warning("The json data is empty.")
            return []
      for element in json_data:
           if element["type"] == "NarrativeText":
            match = find_table_pattern(element['text'])
            if match:
                table_title = match.group(0).strip()
                title = {
                    "title": table_title,
                    "element_id": element["element_id"],
                    "page_number": element["metadata"].get("page_number", None)
                }
                #table_titles[element["metadata"]["parent_id"]] = title
                table_data_list.append(title)
                #TEMPORARY
      
      return table_data_list
    except KeyError as e:
        logger.error(f"KeyError: {e} in JSON data")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e} when processing table pages from the JSON.")
        return []  

def get_table_pages(pdf_path)-> List[int]:
    """ Parses a file to find the pages that contain table(s).
        Returns a list of ints that represent page numbers.
    """
    
    logger = configure_logger(f"{__name__}.get_table_pages")
    try:
        table_page_list = []
        for page_layout in extract_pages(pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    textbox_content = element.get_text()
                    table_match = find_table_pattern(textbox_content)
                    if(table_match):
                        logger.debug("found table match")
                        title = {
                            "title": table_match.group(0).strip(),
                            "page_number": page_layout.pageid
                        }
                        table_page_list.append(title)
    except Exception as e:
        logger.error(f"An error occurred when parsing the file {pdf_path}. Error: {e}")
        return []
    
    return table_page_list

def extract_table_content(textboxes, header_footer_dict) -> List[Dict]:
    logger = configure_logger(f"{__name__}.extract_table_content")

    found_table = False
    table_title = None
    table_textboxes = []
    
    for textbox in textboxes:
        current_text_box = get_element_processor(textbox)
        text_box_text = textbox.get_text()
        if found_table:

                
            #Check current text box to see if it is part of the same table
            #Check if it is part of the header/footer
            #text_box_text = text_box_text.replace("\n", "")
            if(text_box_text in header_footer_dict['header'] or text_box_text in header_footer_dict['footer']):
                logger.debug(f"a header or footer: {text_box_text}")
                continue
            #Check if it is a page number
            if(current_text_box.find_page_number(text_box_text)):
                logger.debug(f"a page number {text_box_text}")
                continue
            
           
            
        match = find_table_pattern(text_box_text)
        if match:
            table_title = match.group(0).strip()
            if(not re.match(r"(continued|cont\.{1}?)", table_title, re.IGNORECASE)):
                table_textboxes.append(textbox)
                logger.debug(f"Found table title: {table_title}")
                found_table = True
        else:
            table_textboxes.append(textbox)
             
    #table_textboxes.sort(key=lambda x: (-x.y0, x.x0))
    return table_textboxes
            