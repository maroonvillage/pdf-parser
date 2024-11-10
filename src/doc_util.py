from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.high_level import extract_pages

def detect_headers_and_footers_pdfminer(pdf_path, header_threshold=0.1, footer_threshold=0.9):
    headers = []
    footers = []

    for page_layout in extract_pages(pdf_path, laparams=LAParams()):
        page_height = page_layout.height

        for element in page_layout:
            if isinstance(element, LTTextBox) or isinstance(element, LTTextLine):
                # Normalize the y-coordinate by the page height
                top_position = element.y1 / page_height

                # If the element is near the top of the page (likely a header)
                if top_position > 1 - header_threshold:
                    headers.append(element.get_text().strip())

                # If the element is near the bottom of the page (likely a footer)
                if top_position < footer_threshold:
                    footers.append(element.get_text().strip())

    return headers, footers

# Example usage
pdf_file_path = "docs/AI_Risk_Management-NIST.AI.100-1.pdf"
headers, footers = detect_headers_and_footers_pdfminer(pdf_file_path)

print("Headers found:")
for header in headers:
    print(header)

print("\nFooters found:")
for footer in footers:
    print(footer)
