from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from io import StringIO

# Open the PDF file
with open('docs/AI_Risk_Management-NIST.AI.100-1.pdf', 'rb') as file:

    # Create a PDF parser object
    parser = PDFParser(file)

    # Create a PDF document object
    document = PDFDocument(parser)

    # Get outlines
    outlines = document.get_outlines()

    # Find the "Method" as an outline item
    method_outline = None
    for level, title, dest, a, se in outlines:
        if title =='Executive Summary' :
            method_outline = (level, title, dest, a, se)
            break

    # Extract the text until the next level 1 outline item
    if method_outline is not None:
        _, method_title, method_dest, _, _ = method_outline
        output_string = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output_string, laparams=None)
        interpreter = PDFPageInterpreter(manager, converter)

        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
            text = output_string.getvalue()
            if method_title in text:
                text = text.split(method_title)[-1]
                output_string = StringIO(text)
            elif '\n1 ' in text:
                # Found another level 1 outline item, stop extracting
                break

        # Print the extracted text
        print(output_string.getvalue())