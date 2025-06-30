import os
from pypdf import PdfReader

def extract_specific_pdf_to_text(pdf_folder_name, pdf_filename, text_filename):
    """
    Reads a specific PDF file from a specified subfolder, extracts text,
    and saves the text to a .txt file in the same subfolder.

    Args:
        pdf_folder_name (str): The name of the subfolder containing the PDF.
                                (e.g., "Resume")
        pdf_filename (str): The name of the PDF file to read.
                            (e.g., "Resume.pdf")
        text_filename (str): The name of the text file to write to.
                             (e.g., "resume.txt")
    """
    try:
        # Get the directory where the current script (test.py) is located
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the folder containing the PDF and text file
        target_folder_path = os.path.join(current_script_dir, pdf_folder_name)

        # Construct the full path to the PDF file
        pdf_full_path = os.path.join(target_folder_path, pdf_filename)

        # Construct the full path to the output text file
        text_full_path = os.path.join(target_folder_path, text_filename)

        print(f"Attempting to read PDF from: {pdf_full_path}")
        print(f"Attempting to write text to: {text_full_path}")

        # Check if the PDF file exists
        if not os.path.exists(pdf_full_path):
            print(f"Error: PDF file not found at '{pdf_full_path}'.")
            return

        # Check if the target folder exists
        if not os.path.isdir(target_folder_path):
            print(f"Error: Target folder '{target_folder_path}' not found or is not a directory.")
            return

        # Read the PDF
        reader = PdfReader(pdf_full_path)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n" # Add newline for readability between pages

        # Write the extracted text to the .txt file
        with open(text_full_path, "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)

        print(f"Successfully extracted text from '{pdf_filename}' to '{text_filename}'.")

    except FileNotFoundError:
        print(f"Error: A file or directory was not found. Please check paths.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- How to use the function for your specific case ---

# Define the relative path to the folder and the file names
pdf_folder = "Resume"
pdf_file = "Resume.pdf"
text_file = "resume.txt"

# Call the function
extract_specific_pdf_to_text(pdf_folder, pdf_file, text_file)