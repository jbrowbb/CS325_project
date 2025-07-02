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




import urllib.parse
import requests
import os

from module_1.DownLoadHelper import DownLoadHelper
from module_1.DownloadArticles import DownloadArticle
from module_2.Gemini import GeminiGenerate
from module_3.testcase import testcase


if __name__ == "__main__":
    # Example usage: Download articles from URLs in a text file
    file_path = 'Data/raw/raw_urls.txt'
    #create a object of DownloadArticle
    url_reader = DownloadArticle()

    #Through the urls to output two file for each articles.
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
    
    Testcase = testcase()
    # filters out homepage/index pages using function
    filtered_urls = Testcase.remove_home_idx_links(urls)
            
    for index, url in enumerate(filtered_urls):
        #print(f"Downloading article from URL: {url}")
        url_reader.download_articles_from_file(url,index) #download the article

        # use the outputed file to generate the summary
        input_path = f"Data/processed/DownLoadFile/article_{index+1}.txt" 
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
        summary_generator = GeminiGenerate()
        GeminiGenerate.configure_genai_with_api_key()
        concise_article = summary_generator.generate_concise_article(article_content)

        # Generate spicy title using the summary if title is not provided
        title = summary_generator.generate_spicy_title(concise_article)
        summary_generator.save_article(title, concise_article,index)

    #some test cases in here.

    #The path of the folder that need count number of word.
    Countwords_folder_path = 'Data/processed/GimiAISummalization'
    #The path of the folder that need count number of files.
    Countnum_folder_path = 'Data/processed'
    #what expected number of files.
    num_files_expected = 10
    #test if we got 20 files.
    Testcase.check_output_files(Countnum_folder_path, num_files_expected)
    #test if the AI generate the right number of words for summary
    word_count_dict=Testcase.count_words_in_files(Countwords_folder_path)
    # Display word count for each file
    for filename, word_count in word_count_dict.items():
        print(f"{filename}: {word_count} words")   
    folder_path = 'Data/processed'