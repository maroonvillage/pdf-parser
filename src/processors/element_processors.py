
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, \
    LTLine, LTRect, LTFigure, LTImage, LTTextLineVertical, LTTextGroup, LTTextGroupTBRL, LTContainer, LTCurve

import logging
import re
from typing import List, Optional
from abc import ABC, abstractmethod
from document import Document, Figure
from matcher_patterns import get_matcher
from utilities.parse_util import replace_extra_space, find_page_number
from pdf_parse_document import Element, Page
from generators.guid_generator import generate_guid

def get_element_processor(element, nlp=None, config=None):
    

    if isinstance(element,LTTextBoxHorizontal):
        return TextBoxProcessor(nlp, config)
    elif isinstance(element,LTTextLineHorizontal):
        return TextLineProcessor()
    elif isinstance(element,LTChar):
        return CharProcessor()
    elif isinstance(element,LTLine):
        return LineProcessor()
    elif isinstance(element,LTRect):
        return RectProcessor()
    elif isinstance(element,LTFigure):
        return FigureProcessor()
    elif isinstance(element,LTImage):
        return ImageProcessor()
    elif isinstance(element,LTTextLineVertical):
        return VerticalLineProcessor()
    elif isinstance(element,LTTextGroup):
        return TextGroupProcessor()
    elif isinstance(element,LTContainer):
        return ContainerProcessor()
    elif isinstance(element,LTTextGroupTBRL):
        return TextGroupTBRLProcessor()
    elif isinstance(element,LTCurve):
        return CurvedLineProcessor()
    else:
        raise ValueError(f"Unsupported element type: {element}")
    
class TextElementProcessor(ABC):
    """Abstract class for processing layout elements."""

    @abstractmethod
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        pass


class TextBoxProcessor(TextElementProcessor):
    """Text box processing"""
    def __init__(self, nlp, config):
      self.nlp = nlp
      self.config = config
    
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        first_line = ''
        line_count = 0
        element_id = generate_guid()
        page_element = Element(element_id, "TextBox")
        
        textbox_content = element.get_text().lstrip().rstrip()
        
        #Check for header/footer text here 
        if(header_footer_text):
            if(textbox_content.replace("\n", "") in header_footer_text):
                return
            
        #Check for page numbers
        if(self.find_page_number(textbox_content)):
            return
        
        page_element.set_content(textbox_content)
        page_element.set_bbox(element.bbox)
        page_element.set_index(element.index)
        page.add_element(page_element)
        
        
        if (textbox_content != ''):
            content_lines_list = textbox_content.split('\n')
            first_line = content_lines_list[0]
            line_count = len(content_lines_list)

        x0, y0, x1, y1 = element.bbox
        width = x1 - x0
        height = y1 - y0
        
        
        
        wfile.write(f"Inside process_element... \n")
        wfile.write("####################################################### \n\n\n")
        
        wfile.write(f"Current Section Header: {current_section_header}\n")
        
        wfile.write(f"Firt Line: {first_line}\n")
        
        wfile.write(f"TextBox Content: {textbox_content}\n")
        
        #Set up matcher ...
        matcher = get_matcher(self.nlp)
        
        #Clean first_line of any leading or trailing spaces and additonal spaces in between
        first_line = replace_extra_space(first_line)

        doc = self.nlp(first_line)
        
        matches = matcher(doc)
        
        found_sections = self._find_sections(first_line)

        if (matches or found_sections != []):
            current_section_header = first_line
            wfile.write(f"Found section(s): {current_section_header} ... count {len(found_sections)} \n")
            section_match = self._find_section(current_section_header, matching_groups=True)
            if (section_match is not None):
                section_match_text = section_match.group(0) #Get the full match
                wfile.write(f"Section Match found: {section_match_text}\n")
                if (section_match.group(2) is not None):
                    
                    group_match = section_match.group(2)
                    #current_section_header = f'{section_match.group(1).strip()} {section_match.group(2).strip()}'
                    wfile.write(f'Group 1: -{section_match.group(1).lstrip().rstrip()}-')
                    wfile.write(f'Group 2: -{group_match.lstrip().rstrip()}-')
                    current_section = document.find_section_by_heading(group_match.lstrip().rstrip())
                    if (current_section is not None):
                        wfile.write(f'Found section object: {current_section}')
                        current_section_header = f'{section_match.group(1).strip()} {section_match.group(2).strip()}'
                        current_section.heading = current_section_header
                else:
                    wfile.write(f"Group 2 NOT found.\n")
            else:
                current_section = document.find_section_by_heading(current_section_header)

            if (line_count > 1):
                if (current_section is not None):
                    #current_section.add_paragraph("\n".join(content_lines_list[1:]))
                    current_section.add_paragraph(textbox_content)

            line_count = 0
        elif self._find_appendicies(first_line) != []:
                wfile.write(f"Found appendix {textbox_content}\n")
                next_line = ''
                wfile.write(f"Appendix pattern {self._find_appendix(first_line).group()} ... first line: {first_line} \n")
                #pattern_match = self._find_appendix(first_line).group()
                #if (pattern_match == first_line):
                #    wfile.write(f"re match is equal to first line: {self._find_appendix(first_line).group()} {first_line}\n")
                #    if (line_count > 1):
                #        next_line = content_lines_list[1]
                #        first_line = f'{first_line} {next_line.lstrip().rstrip()}'
                current_section_header = first_line.strip()
                #wfile.write(f"appendix wrapped across 2 lines: {next_line}\n")
                current_section = document.find_section_by_heading(current_section_header)

                if (current_section is not None):
                    #current_section.add_paragraph("\n".join(content_lines_list[1:]))
                    current_section.add_paragraph(textbox_content)
        elif self._find_figures(first_line) != []:
            wfile.write(f"Found figure {textbox_content}\n")
            current_section = document.find_section_by_heading(current_section_header)
            #if (current_section_header != '' and document.find_section_by_heading(current_section_header) is not None):
            if (current_section is not None):
                    wfile.write(f"Found corresponding section header for figure:  {current_section_header}\n")
                    #current_section = document.find_section_by_heading(current_section_header)
                    current_section.add_figure(Figure(textbox_content))
        else:
            if (current_section_header != ''):
                wfile.write(f"In else.  No section, appendicies or figures found:  {current_section_header}\n")
                current_section = document.find_section_by_heading(current_section_header)
                if (current_section is not None):
                    wfile.write(f"Found current_section object {current_section}\n")
                    current_section.add_paragraph(textbox_content)
                    
        wfile.write(f"Leaving process_element scope!\n")
        wfile.write("####################################################### \n\n\n")
        
        return current_section_header

    def find_sections(self, text: str, matching_groups: bool = False) -> List[str]:
        return self._find_sections(text, matching_groups)
    
    def find_section(self, text: str, matching_groups=False):
        return self._find_section(text, matching_groups)
    
    def find_appendicies(self, text: str) -> List[str]:
        return self._find_appendicies(text)
    
    def find_appendix(self, text: str) -> Optional[re.Match]:
        return self._find_appendix(text)
    
    def find_figures(self, text: str) -> List[str]:
        return self._find_figures(text)
    
    def find_page_number(self, text: str) -> Optional[re.Match]:
        return self._find_page_number(text)
            
    def _find_sections(self, text: str, matching_groups: bool = False) -> List[str]:
        """
        Finds all occurrences of section patterns within the given text.

        Parameters:
            text (str): The text to search in.
            matching_groups (bool): If True, return re.findall with matching groups, else without matching groups.

        Returns:
            List[str]: A list of all matched strings or an empty list if no matches are found.
        """
        log = logging.getLogger(__name__)
        try:
            section_pattern = r"^(?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
            section_pattern_with_matching_groups = r"^((?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
            
            if matching_groups:
                matches = re.findall(section_pattern_with_matching_groups, text)
                log.debug(f"Matching with groups pattern: {section_pattern_with_matching_groups} on text: '{text}'. Result: {matches}")
                return matches
            else:
                matches = re.findall(section_pattern, text)
                log.debug(f"Matching with section pattern: {section_pattern} on text: '{text}'. Result: {matches}")
                return matches
        except re.error as e:
            log.error(f"Regex error: {e} with input text: {text}")
            return []
        except Exception as e:
            log.error(f"An unexpected error has occurred: {e} with input text: {text}")
            return []

    def _find_section(self, text: str, matching_groups=False):
        """
        Attempts to match section patterns within the given text.

        Parameters:
            text (str): The text to search in.
            matching_groups (bool): If True, return re.match else re.findall

        Returns:
            re.Match or list or None : return re.Match or list if matched else return None
        """
        log = logging.getLogger(__name__)
        try:
            section_pattern = r"^(?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*\s+[A-Za-z][\w\s\-\,]+"
            section_pattern_with_matching_groups = r"^((?:\d+\.{0,1})(?:\d+)*(?:\.\d+)*)(\s+[A-Za-z][\w\s\-\,]+)"
            
            if matching_groups:
                match = re.match(section_pattern_with_matching_groups, text)
                log.debug(f"Matching with groups pattern: {section_pattern_with_matching_groups} on text: '{text}'. Result: {match}")
                return match
            else:
                match = re.match(section_pattern, text)
                log.debug(f"Matching with section pattern: {section_pattern} on text: '{text}'. Result: {match}")
                return match

        except re.error as e:
            log.error(f"Regex error: {e} with input text: {text}")
            return None
        except Exception as e:
            log.error(f"An unexpected error has occurred: {e} with input text: {text}")
            return None
    
    def _find_appendicies(self, text: str) -> List[str]:
        """
        Finds all occurrences of appendix patterns within the given text.

        Parameters:
            text (str): The text to search in.

        Returns:
            List[str]: A list of all matched strings or an empty list if no matches are found.
        """
        log = logging.getLogger(__name__)
        try:
            appendix_pattern = r"^(Appendix|Annex)\s+[A-Z]\.*"  #Simplified regex pattern
            matches = re.findall(appendix_pattern, text, re.IGNORECASE)
            log.debug(f"Matching with appendix pattern: {appendix_pattern} on text: '{text}'. Result: {matches}")
            return matches
        except re.error as e:
            log.error(f"Regex error: {e} with input text: {text}")
            return []
        except Exception as e:
            log.error(f"An unexpected error has occurred: {e} with input text: {text}")
            return []
    
    def _find_appendix(self, text: str) -> Optional[re.Match]:
        """
        Attempts to match an appendix pattern at the beginning of the given text.

        Parameters:
            text (str): The text to search in.

        Returns:
            Optional[re.Match]: A match object if a match is found, otherwise None.
        """
        log = logging.getLogger(__name__)
        try:
            appendix_pattern = r"^(Appendix|Annex)\s+[A-Z]\.*" #Simplified regex pattern
            match = re.match(appendix_pattern, text, re.IGNORECASE)
            log.debug(f"Matching with appendix pattern: {appendix_pattern} on text: '{text}'. Result: {match}")
            return match
        except re.error as e:
            log.error(f"Regex error: {e} with input text: {text}")
            return None
        except Exception as e:
            log.error(f"An unexpected error has occurred: {e} with input text: {text}")
            return None

    def _find_figures(self, text: str) -> List[str]:
        """
        Finds all occurrences of figure patterns within the given text.

        Parameters:
            text (str): The text to search in.

        Returns:
            List[str]: A list of all matched strings or an empty list if no matches are found.
        """
        log = logging.getLogger(__name__)
        try:
            figure_pattern = r"^Figure\s\d+|Fig\.\s\d+"
            matches = re.findall(figure_pattern, text, re.IGNORECASE)
            log.debug(f"Matching with figure pattern: {figure_pattern} on text: '{text}'. Result: {matches}")
            return matches
        except re.error as e:
            log.error(f"Regex error: {e} with input text: {text}")
            return []
        except Exception as e:
            log.error(f"An unexpected error has occurred: {e} with input text: {text}")
            return []
    
    def _find_page_number(self, text: str) -> Optional[re.Match]:
        """
        Attempts to match a page number pattern at the end of the given text.

        Parameters:
            text (str): The text to search in.

        Returns:
            Optional[re.Match]: A match object if a match is found, otherwise None.
        """
        log = logging.getLogger(__name__)
        try:
            return find_page_number(text)
        except re.error as e:
            log.error(f"Regex error: {e} with input text: {text}")
            return None
        except Exception as e:
            log.error(f"An unexpected error has occurred: {e} with input text: {text}")
            return None


class TextLineProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        element_id = generate_guid()
        page_element = Element(element_id, "TextLine")
        page_element.set_bbox(element.bbox)
        page.add_element(page_element)
        wfile.write(f"TextLine: {element.bbox}\n")

class CharProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        wfile.write(f"Character: {element.get_text()}, Font: {element.fontname}, Size: {element.size}\n")

class LineProcessor(TextElementProcessor):
     def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        element_id = generate_guid()
        page_element = Element(element_id, "Line")
        page_element.set_bbox(element.bbox)
        page.add_element(page_element)
        wfile.write(f"Line from ({element.x0}, {element.y0}) to ({element.x1}, {element.y1})\n")

class RectProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        element_id = generate_guid()
        page_element = Element(element_id, "Rectangle")
        page_element.set_bbox(element.bbox)
        page.add_element(page_element)
        wfile.write(f"Rectangle with bounding box: ({element.x0}, {element.y0}) - ({element.x1}, {element.y1})\n")

class FigureProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        element_id = generate_guid()
        page_element = Element(element_id, "Figure")
        page_element.set_bbox(element.bbox)
        page_element.set_content(element.matrix)
        page.add_element(page_element)
        wfile.write(f"Figure with width {element.width} and height {element.height}\n")

class ImageProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        wfile.write(f"Image found with size: {element.srcsize} \n")

class VerticalLineProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        wfile.write(f"Vertical line found: {element.get_text()} \n")

class TextGroupProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        wfile.write(f"Text Group found: {element.get_text()} \n")

class ContainerProcessor(TextElementProcessor):
    def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
        wfile.write(f"Found CONTAINER ... {element.bbox}\n")

class TextGroupTBRLProcessor(TextElementProcessor):
     def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
         wfile.write(f"Found Text Group TBRL ... {element.bbox}\n")
class CurvedLineProcessor(TextElementProcessor):
     def process_element(self, element, document: Document, current_section_header: str, wfile, page: Page, header_footer_text: str=None):
         wfile.write(f"Found Curved Line found ... {element.bbox}\n")