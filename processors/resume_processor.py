import os
import json

# Relative imports from other packages
from scrapers.pdf_scraper import extract_text_from_pdf
from ai.gemini_analyzer import analyze_resume # Use the new name
from core.data_cleaner import clean_filename
from core.file_manager import ensure_directory_exists, save_text_file, save_json_file

# --- Configuration ---
RESUME_FOLDER = "Resume" # Define here as it's specific to resume processing

def process_single_resume(pdf_filename):
  
    ensure_directory_exists(RESUME_FOLDER) # Ensure Resume folder exists

    pdf_path = os.path.join(RESUME_FOLDER, pdf_filename)

    # Derive output filenames using clean_filename
    base_name = os.path.splitext(pdf_filename)[0]
    scraped_txt_filename = f"{clean_filename(base_name)}_scraped.txt"
    summary_json_filename = f"{clean_filename(base_name)}_summary.json"

    scraped_txt_path = os.path.join(RESUME_FOLDER, scraped_txt_filename)
    summary_json_path = os.path.join(RESUME_FOLDER, summary_json_filename)

    print(f"\n--- Processing Resume: {pdf_path} ---")

    # Check if the PDF exists before proceeding
    if not os.path.exists(pdf_path):
        print(f"Error: Resume PDF '{pdf_filename}' not found at {pdf_path}. Skipping.")
        return

    resume_content = extract_text_from_pdf(pdf_path)

    if resume_content:
        print("Text extraction successful.")

        # Save scraped text using file_manager
        if not save_text_file(scraped_txt_path, resume_content):
            return # Exit if saving fails

        print("Sending scraped text to Gemini for resume analysis...")
        analysis_result = analyze_resume(resume_content) # Call the renamed function

        if analysis_result:
            print("Gemini analysis successful.")

            # Save the full AI analysis (summary + extracted data) as JSON using file_manager
            if save_json_file(summary_json_path, analysis_result):
                print("\n--- Summary Snippet from JSON Output ---")
                # Safely access dictionary elements using .get()
                print("Job Experiences Summary:\n", analysis_result.get('summaries', {}).get('job_experiences_summary', 'N/A'))
                print("\nSkills Summary:\n", analysis_result.get('summaries', {}).get('skills_summary', 'N/A'))
                print("\nSuggested Job Titles:\n", ", ".join(analysis_result.get('extracted_data', {}).get('suggested_job_titles', [])))
                print("\nSuggested Locations:\n", ", ".join(analysis_result.get('extracted_data', {}).get('suggested_locations', [])))
            else:
                print("Failed to save summarized resume (JSON).") # save_json_file already prints error
        else:
            print("Failed to get analysis from Gemini for the resume.")
    else:
        print("Failed to extract text from PDF resume.")