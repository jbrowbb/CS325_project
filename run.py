import os
from module_1.pdf_extractor import PDFExtractor
from module_2.file_handler import FileHandler


if __name__ =="__main__":
    # Gets current directory where script location is
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # Path to the 'Resume' folder
    resume_folder_path = os.path.join(current_script_directory, "Resume")

    # Full paths for the input PDF and output TXT files
    pdf_input_path = os.path.join(resume_folder_path, "Resume.pdf")
    txt_output_path = os.path.join(resume_folder_path, "resume.txt")

    print(f"Attmepting to read PDF from: {pdf_input_path}")
    print(f"Attempting to write text to: {txt_output_path}")


    # Create instances for worker classes
    pdf_extractor = PDFExtractor()
    file_handler = FileHandler()


    # Extracts text from the PDF
    extracted_text = pdf_extractor.extract_text_from_pdf(pdf_input_path)

    if extracted_text.startswith("Error:"):
        print(f"Failed to extract text: {extracted_text}")
    else:
        success = file_handler.write_text_to_file(txt_output_path, extracted_text)

        if success:
            print(f"Successfully extracted text from 'Resume.pdf' and saved to '{txt_output_path}'.")
        else:
            print(f"Failed to save extracted text to '{txt_output_path}'. Check console for errors.")