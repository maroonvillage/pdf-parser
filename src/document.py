import json
import re
from typing import List, Dict, Any

class Row:
    def __init__(self, cells: Dict[str, Any]):
        """
            Initializes a new Row object.

            Parameters:
                cells (Dict[str, Any]): a dictionary containing the cells.
        """
        self.cells = cells
       
    def to_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of the row.

            Returns:
              Dict[str,Any]: A dictionary representation of the Row.
        """
        return self.cells
        
class Figure:
    def __init__(self, caption):
        self.caption = caption

class Table:
    def __init__(self, title):
        """
            Initializes a new Table object.

            Parameters:
                title (str): The table title.
        """
        self._title = title
        self.rows = []
        
    @property 
    def title(self) -> str: 
        """Getter method for table title"""
        return self._title 
    
    @title.setter 
    def title(self, value) -> None:
        """Setter method for title"""
        self._title
        
    
    def add_row(self, row):
        """
        Adds a row to the table, using the row dictionary.

            Parameters:
                 row (Dict[str, Any]): The row object containing the data for each cell.
        """
        self.rows.append(row)
    
    def to_dict(self) -> Dict[str, Any]:
        """
           Returns a dictionary representation of the table.

           Returns:
                Dict[str, Any]: A dictionary containing all table data.
        """
        return {
            "title": self._title,
            "rows": [row.to_dict() for row in self.rows],
        }      

class Section:
    def __init__(self, heading):
        self.heading = heading
        self.paragraphs = []
        self.figures = []
        self.tables = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def add_figure(self, figure):
        self.figures.append(figure)

    def add_table(self, table):
        self.tables.append(table)

class Document:
    def __init__(self, title, content):
        self.title = title
        self.sections = content

    def add_section(self, section):
        self.sections.append(section)

    # Method to find a section by title
    def find_section_by_heading(self, heading):
        if heading is None:
            return None
        # Define the regex pattern to match the specific pattern in the heading
        clean_heading = re.sub(r'[\W_]+$', '', heading)
        pattern = fr'\b{clean_heading}\b'
        
        for section in self.sections:
            # Use re.search to find the pattern in the text 
            match = re.search(pattern, section.heading, re.IGNORECASE)
            
            if match:
                return section
        return None  # If no section with the given title is found
    
    #@classmethod
    def to_dict(self):
        return {
            "title": self.title,
            "sections": [
                {
                    "heading": section.heading,
                    "paragraphs": section.paragraphs,
                    "figures": [{"caption": fig.caption} for fig in section.figures],
                    "tables": [{"title": table.title} for table in section.tables]
                }
                for section in self.sections
            ]
        }

    #@classmethod 
    def from_dict(cls, data): 
        return cls(data["title"], data["sections"])
                                       
    #@classmethod
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def __repr__(self): 
        return f"Document(title={self.title}, content={self.sections})"