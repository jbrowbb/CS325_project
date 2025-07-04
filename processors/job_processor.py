import os
import json
import re # Only for company name

# Relative imports from other packages
from scrapers.web_scraper import scrape_website_to_plain_text
from ai.gemini_analyzer import analyze_job_description # Use the new name
from core.data_cleaner import clean_filename
from core.file_manager import ensure_directory_exists, save_text_file, load_urls_from_file, save_json_file

# --- Configuration ---
JOB_FOLDER = "Jobs" # Define here
JOB_URLS_FILE = os.path.join(JOB_FOLDER, "urls.txt")
JOB_GENERAL_FOLDER = os.path.join(JOB_FOLDER, "General")
JOB_SUMMARIZED_FOLDER = os.path.join(JOB_FOLDER, "Summarized")

def process_job_urls():
    """
    Reads URLs from a file, scrapes job descriptions, and analyzes them,
    saving raw text to General folder and JSON summaries to Summarized folder.
    """
    # Ensure all necessary job folders exist
    ensure_directory_exists(JOB_FOLDER)
    ensure_directory_exists(JOB_GENERAL_FOLDER)
    ensure_directory_exists(JOB_SUMMARIZED_FOLDER)

    # Load URLs using file_manager
    urls, error = load_urls_from_file(JOB_URLS_FILE)
    if error:
        print(error)
        print(f"Please create this file inside the '{JOB_FOLDER}' folder and add one URL per line.")
        return

    print(f"\n--- Processing Job URLs from: {JOB_URLS_FILE} ---")
    urls_processed = 0
    urls_failed = 0

    if not urls:
        print("No URLs found in the file. Please add URLs to process.")
        return

    for url in urls:
        urls_processed += 1
        print(f"\n--- Processing Job URL ({urls_processed}): {url} ---")
        scraped_jd_content, scrape_error = scrape_website_to_plain_text(url)

        if scraped_jd_content:
            print("Website scraping successful. Saving raw text to General folder...")

            # Use a cleaned version of the URL as a base for the filename for raw text
            url_hash = str(hash(url)) # Use hash to ensure uniqueness for long URLs
            general_filename_base = clean_filename(url_hash + '_' + url.split('://')[-1].split('/')[0])
            general_txt_path = os.path.join(JOB_GENERAL_FOLDER, f"{general_filename_base}_scraped.txt")

            # Save raw scraped text using file_manager
            if not save_text_file(general_txt_path, scraped_jd_content):
                urls_failed += 1
                continue # Skip AI analysis if we can't save the raw text

            print("Sending scraped text to Gemini for job description analysis...")
            analysis_result = analyze_job_description(scraped_jd_content) # Call the renamed function

            if analysis_result:
                print("Gemini analysis successful. Saving summarized JSON to Summarized folder...")

                # Try to get a better filename from the extracted job title and company if available
                job_title_for_filename = analysis_result.get('extracted_data', {}).get('job_title', None)
                company_name_from_summary = None
                summary_text = analysis_result.get('summary', '')
                if " at " in summary_text: # Heuristic to try and get company name
                    parts = summary_text.split(" at ", 1)
                    if len(parts) > 1:
                        company_name_match = re.match(r'^\w+', parts[1].strip())
                        if company_name_match:
                            company_name_from_summary = company_name_match.group(0)

                if job_title_for_filename:
                    if company_name_from_summary:
                        final_filename_base = clean_filename(f"{job_title_for_filename}_{company_name_from_summary}")
                    else:
                        final_filename_base = clean_filename(job_title_for_filename)
                else:
                    final_filename_base = general_filename_base # Fallback to URL-based name

                summary_json_path = os.path.join(JOB_SUMMARIZED_FOLDER, f"{final_filename_base}_summary.json")

                # Save the full AI analysis (summary + extracted data) as JSON using file_manager
                if save_json_file(summary_json_path, analysis_result):
                    print("\n--- Job Description Summary Snippet ---")
                    # Safely access dictionary elements using .get()
                    print("Job Title:", analysis_result.get('extracted_data', {}).get('job_title', 'N/A'))
                    print("Location:", analysis_result.get('extracted_data', {}).get('location', 'N/A'))
                    print("Pay Range:", analysis_result.get('extracted_data', {}).get('pay_range', 'N/A'))
                    print("Summary:\n", analysis_result.get('summary', 'N/A'))
                else:
                    print("Failed to save summarized job description (JSON).") # save_json_file already prints error
                    urls_failed += 1
            else:
                print("Failed to get analysis from Gemini for this job description.")
                urls_failed += 1
        else:
            print(f"Failed to scrape job description from {url}: {scrape_error}")
            urls_failed += 1

    print(f"\n--- Job Description Processing Complete: {urls_processed} URLs attempted, {urls_failed} failed ---")