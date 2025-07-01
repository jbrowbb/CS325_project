# Input: Path to the single PDF file
# OUtput: Extracted text content of the PDF

import os
from pypdf import PdfReader

class PDFExtractor:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        if not os.path.exists(pdf_path):
            return F"Error: PDF file not found at '{pdf_path}'."
        if not pdf_path.lower().endswith(".pdf"):
            return f"Error: '{pdf_path}' is not a PDF file."
        

        try:
            reader = PdfReader(pdf_path)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()

                if text:    # Append text only if successfully extracted
                    extracted_text += text + "\n"
                
            return extracted_text.strip()   # removes any trailing whitespace
        
        except Exception as e:
            return f"Error occured while extracting text from {pdf_path}: {str(e)}"