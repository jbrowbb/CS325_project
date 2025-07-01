# run.py
# Main script to read a PDF and save its content to a text file.
# SOLID Principle Focus: This script acts as a high-level orchestrator,
# depending on the concrete implementations of PDFExtractor and FileHandler.
# While not strictly demonstrating DIP via explicit interfaces here (to simplify the single-file concept),
# it still separates concerns across modules.

import os
from module_1.pdf_extractor import PDFExtractor # Import the PDF extraction logic
from module_2.file_handler import FileHandler   # Import the file I/O logic

if __name__ == "__main__":
    # Get the directory where the current script (run.py) is located
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the 'Resume' folder, relative to run.py
    resume_folder_path = os.path.join(current_script_dir, "Resume")

    # Define the full paths for the input PDF and output TXT files
    pdf_input_path = os.path.join(resume_folder_path, "Resume.pdf")
    txt_output_path = os.path.join(resume_folder_path, "resume.txt")

    print(f"Attempting to read PDF from: {pdf_input_path}")
    print(f"Attempting to write text to: {txt_output_path}")

    # Create instances of our worker classes
    pdf_extractor = PDFExtractor()
    file_handler = FileHandler()

    # Step 1: Extract text from the PDF
    extracted_text = pdf_extractor.extract_text_from_pdf(pdf_input_path)

    if extracted_text.startswith("Error:"):
        print(f"Failed to extract text: {extracted_text}")
    else:
        # Step 2: Write the extracted text to the output file
        success = file_handler.write_text_to_file(txt_output_path, extracted_text)
        if success:
            print(f"Successfully extracted text from 'Resume.pdf' and saved to '{txt_output_path}'.")
        else:
            print(f"Failed to save extracted text to '{txt_output_path}'. Check console for errors.")