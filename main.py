# my_ai_project/main.py
import os
import time # Import time for potential short pauses if desired

# Import processing functions from the new processors package
from processors.resume_processor import process_single_resume, RESUME_FOLDER
from processors.job_processor import process_job_urls, JOB_FOLDER, JOB_URLS_FILE

# --- Main execution flow ---
if __name__ == "__main__":
    print("--- Starting AI Job Analyzer Workflow ---")
    print("This program will first process your resume, then guide you to add job URLs.")

    # --- Configuration ---
    # For Resume Processing
    # <<< IMPORTANT: CHANGE THIS to your actual resume PDF file name inside the 'Resume' folder
    TEST_RESUME_PDF_FILENAME = "Resume.pdf"

    # --- Step 1: Process Resume ---
    print("\n--- Step 1: Processing Resume ---")
    resume_pdf_full_path = os.path.join(RESUME_FOLDER, TEST_RESUME_PDF_FILENAME)

    if os.path.exists(resume_pdf_full_path):
        process_single_resume(TEST_RESUME_PDF_FILENAME)
    else:
        print(f"Resume PDF '{TEST_RESUME_PDF_FILENAME}' not found in the '{RESUME_FOLDER}' folder.")
        print("Skipping resume processing for now. Please place your resume PDF there if you wish to analyze it.")
        # Optionally, you could add a pause here too if resume is missing

    # --- Step 2: Prompt User for Job URLs ---
    print("\n--- Step 2: Prepare Job URLs ---")
    print(f"Please now open the file: '{JOB_URLS_FILE}'")
    print("Add the Indeed.com or LinkedIn.com job description URLs (one per line) you wish to analyze.")
    print("Save the file after adding all URLs.")

    # Keep prompting until the user confirms
    input("\nPRESS ENTER to continue once you have updated and saved the 'indeed_urls.txt' file...")
    print("Thank you. Proceeding with job description analysis.")
    time.sleep(1) # Small pause for better user experience

    # --- Step 3: Process Job Descriptions ---
    print("\n--- Step 3: Processing Job Descriptions ---")
    process_job_urls()

    print("\n--- All Workflow Steps Complete ---")
    print("You can find the processed files in the 'Resume/' and 'Job/General/' and 'Job/Summarized/' folders.")