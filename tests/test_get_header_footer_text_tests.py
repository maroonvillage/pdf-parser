
from ..src.utilities.parse_util import get_header_footer_text


def test_get_header_footer_text_doc1():
    
    pdf_path  = 'docs/AI_Risk_Management-NIST.AI.100-1.pdf'
    
    assert  get_header_footer_text(pdf_path) != None

def test_get_header_footer_text_doc2():
    
    pdf_path  = 'docs/ISO+IEC+23894-2023.pdf' 
    
    assert get_header_footer_text(pdf_path) != None