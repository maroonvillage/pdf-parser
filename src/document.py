import json
import re
#from parse_util import strip_non_alphanumeric

class Figure:
    def __init__(self, caption):
        self.caption = caption

class Table:
    def __init__(self, title):
        self.title = title

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