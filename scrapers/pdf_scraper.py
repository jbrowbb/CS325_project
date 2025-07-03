import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or "" # Handle potential None if page is empty
        return text
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return None
    except Exception as e:
        print(f"An error occurred during PDF text extraction: {e}")
        return None