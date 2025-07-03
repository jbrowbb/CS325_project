from pypdf import PdfReader # Import PdfReader from pypdf

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file using pypdf."""
    text = ""
    try:
        # Create a PdfReader object
        reader = PdfReader(pdf_path)

        # Iterate over each page and extract text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text: # Ensure text is not None or empty
                text += page_text + "\n" # Add a newline between pages for readability

        return text.strip() # Remove any leading/trailing whitespace

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return None
    except Exception as e:
        print(f"An error occurred during PDF text extraction with pypdf: {e}")
        return None