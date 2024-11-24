import json

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
    def __init__(self, title):
        self.title = title
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    # Method to find a section by title
    def find_section_by_heading(self, heading):
        for section in self.sections:
            if section.heading.endswith(heading):
                return section
        return None  # If no section with the given title is found
    
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

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)