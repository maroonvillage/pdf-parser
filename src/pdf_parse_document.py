import json
from typing import List

class Element:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.content = None
        self.bbox = None
        self.width = None
        self.height = None
        self.index = None
        
    
    def set_content(self, content):
        self.content = content
        
    def set_bbox(self, bbox):
        self.bbox = bbox
        
    def set_width(self, width):
        self.width = width
        
    def set_height(self, height):    
        self.height = height   
        
    def set_index(self, index):
        self.index = index 
        
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "bbox": self.bbox,
            "width": self.width,
            "height": self.height,
            "index": self.index
        }
    def __repr__(self):
       """Returns a detailed string representation of the Element."""
       return self.__str__()        
   
class Page:
    def __init__(self, id, number):
        self.page_id = id
        self.number = number
        self.bbox = None
        self.elements = []
        
    def set_bbox(self, bbox):
        self.bbox = bbox
            
    def add_element(self, element):
        self.elements.append(element)
        
    def to_dict(self):
        return {
            "number": self.number,
            "page_id": self.page_id,
            "elements": [element.to_dict() for element in self.elements]
        }
        
class PDFParseDocument:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        
    def add_page(self, page):
        self.pages.append(page)
        
    def to_dict(self):
        return {
            "title": self.title,
            "pages": [page.to_dict() for page in self.pages]
        }
        
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
        
    def __repr__(self):
        return self.__str__()