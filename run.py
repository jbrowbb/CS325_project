import urllib.parse
import requests
import os
from module_1.DownloadHelper import DownLoadHelper
from module_1.download_website import DownloadJob
from module_2.gemini import GeminiGenerateJobs
from module_2.gemini import GeminiGenerateResume
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


    file_path = 'Jobs/urls.txt'
    #create a object of DownloadArticle
    url_reader = DownloadJob()

    try: 
        with open(file_path, 'r') as file:
            urls = file.readlines() #read every url
            urls = [url.strip() for url in urls]    # strips whitespace

        # Check if the list is empty after stripping whitespace
        if not urls:
            print(f"Error: No URLs found in '{file_path}'. The file might be empty or contain only whitespace.")
            exit()
    except FileNotFoundError as e:
        # Handle the error if the input file for urls is not found
        error_message = f"Error: {e.filename} not found."
        print(error_message)
        exit()
            
    for index, url in enumerate(filtered_urls):
        
        url_reader.download_articles_from_file(url,index)

        # use the outputed file to generate the summary
        input_path = f"Job/General/job_{index+1}.txt" 
        try: 
            with open(input_path, "r") as file:
                lines = file.readlines()
                article_content = "".join(lines[0:]) if len(lines) > 1 else ""
        except FileNotFoundError as e:
            # Handle the error if the input file for article is not found
            error_message = f"Error: {e.filename} not found."
            print(error_message)
            exit()
        if not article_content:
            print("Error: No content found in input file.")

        # Generate the sumary for present article
        summary_generator = GeminiGenerateJobs()
        GeminiGenerateJobs.configure_genai_with_api_key()
        concise_job = summary_generator.generate_concise_job(job_content)

        title = summary_generator.generate_spicy_title(concise_job)
        summary_generator.save_job(title, concise_job,index)
