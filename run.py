import os
from pypdf import PdfReader

def extract_pdf_text(pdf_foldername, pdf_filename, text_filename):

    try:
        # Gets the directory of the current script location
        current_script_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the folder containing the PDF and text file
        target_folder_path = os.path.join(current_script_directory, pdf_foldername)

        # Full path to the PDF file
        pdf_full_path = os.path.join(target_folder_path, pdf_filename)

        # Full path to the output text file
        text_full_path = os.path.join(target_folder_path, text_filename)

        if not os.path.exists(pdf_full_path):
            print(f"Error: PDF file not found at '{pdf_full_path}'.")
            return
        
        # Check if target folder exists
        if not os.path.isdir(target_folder_path):
            print(f"Error: Target folder '{target_folder_path}' not found or is not in directory.")
            return
        

        # Reads the PDF
        reader = PdfReader(pdf_full_path)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"

        # Writes the extracted text to the txt file
        with open(text_full_path, 'w', encoding="utf-8") as text_file:
            text_file.write(extracted_text)

        print(f"Successfully extracted text from '{pdf_filename}' to '{text_filename}'.")


    except FileNotFoundError:
        print(f"Error: A file or directory was not found. Please check paths.")

    except Exception as e:
        print(f"An error occured: {e}")



# Define the relative path to the folder and the file names
pdf_folder = "Resume"
pdf_file = "Resume.pdf"
text_file = "resume.txt"


# Call the funciton
extract_pdf_text(pdf_folder, pdf_file, text_file)