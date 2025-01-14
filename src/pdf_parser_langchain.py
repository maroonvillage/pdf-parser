from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PDFMinerLoader




"""
def extract_text_pdfminer(pdf_path):

    loader = PDFMinerLoader(pdf_path)

    docs = loader.load()
    docs[0]
    #print(len(docs))

    if(len(docs) == 1):
        return docs[0]
"""


def extract_text_line_by_line_pdfminer(pdf_path):

    pdf_loader = PDFMinerLoader(pdf_path)


    # Load the document
    documents = pdf_loader.load()

    #print(documents)
        
    for document in documents: 
        lines = document.page_content.splitlines()

    line_no = 1

    for line in lines:
        if(line != ''):
            print(f" Line # {line_no}: {line}")
        else:
            print(f" Line # {line_no}: empty-line")
        #print(line)
        print()
        line_no += 1