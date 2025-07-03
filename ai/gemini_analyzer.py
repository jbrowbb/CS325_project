import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash" # Generally good balance of cost and capability

def analyze_resume(resume_text): # RENAMED from analyze_resume_with_gemini
    """
    Uses Gemini to extract job experiences, skills, job titles, and locations,
    and then summarizes them from a resume.
    """
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
    You are an expert resume analyzer. Your task is to extract specific information from the provided resume text and then summarize key sections.

    **Instructions:**
    1.  **Extract Job Experiences:** For each job experience, identify the job title, company name, start date, end date (or "Present"), and a concise summary of responsibilities/achievements.
    2.  **Extract Skills:** List all technical and soft skills. Categorize them if possible (e.g., "Programming Languages", "Tools", "Soft Skills").
    3.  **Identify Job Titles to Look For:** Based on the extracted job titles and the overall career trajectory, suggest potential future job titles a person with this resume might be interested in, focusing on those that indicate career progression or lateral moves.
    4.  **Identify Locations to Look For:** Based on the locations mentioned in work experience or education, suggest potential geographic locations where this person might seek new opportunities.
    5.  **Summarize Job Experiences:** Provide a concise, bullet-point summary of the candidate's professional work history, highlighting their progression and key contributions.
    6.  **Summarize Skills:** Provide a brief overview of the candidate's core competencies.

    **Output Format (JSON):**
    ```json
    {{
        "extracted_data": {{
            "job_experiences": [
                {{
                    "job_title": "...",
                    "company": "...",
                    "start_date": "...",
                    "end_date": "...",
                    "responsibilities_summary": "..."
                }}
                // ... more job experiences
            ],
            "skills": {{
                "technical": [
                    "skill1", "skill2"
                ],
                "soft_skills": [
                    "skillA", "skillB"
                ],
                "other": [
                    "skillX"
                ]
            }},
            "suggested_job_titles": [
                "Suggested Job Title 1",
                "Suggested Job Title 2"
            ],
            "suggested_locations": [
                "City, State",
                "Another City, Country"
            ]
        }},
        "summaries": {{
            "job_experiences_summary": "Concise summary of professional experience in bullet points.",
            "skills_summary": "Brief overview of core competencies."
        }}
    }}
    ```

    **Resume Text:**
    {resume_text}
    """
    return _call_gemini_api(prompt)

def analyze_job_description(job_description_text): # RENAMED from analyze_job_description_with_gemini
    """
    Uses Gemini to extract and summarize key information from a job description.
    """
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
    You are an AI assistant specialized in analyzing job descriptions.
    Your task is to extract the following key information from the provided job description and then summarize it.

    **Instructions:**
    1.  **Extract Job Title:** Identify the primary job title.
    2.  **Extract Skills Needed:** List all technical and soft skills explicitly mentioned or clearly implied as required.
    3.  **Extract Pay/Salary Range:** Identify any mentioned salary range or pay information. If none, state "Not specified". Provide as a concise string (e.g., "$80,000 - $100,000/year" or "Competitive, equity options").
    4.  **Extract Location:** Identify the primary work location(s) mentioned (city, state, country, or remote status). Provide as a concise string (e.g., "New York, NY, USA", "Remote", "London, UK").
    5.  **Summarize Job Description:** Provide a concise, 3-5 sentence summary of the main responsibilities and overall scope of the role.

    **Output Format (JSON):**
    ```json
    {{
        "extracted_data": {{
            "job_title": "...",
            "skills_needed": [
                "skill1",
                "skill2"
            ],
            "pay_range": "...",
            "location": "..."
        }},
        "summary": "..."
    }}
    ```

    **Job Description Text:**
    {job_description_text}
    """
    return _call_gemini_api(prompt)

def _call_gemini_api(prompt):
    """Helper function to call Gemini API and handle common errors."""
    model = genai.GenerativeModel(MODEL_NAME)
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1 # Lower temperature for more factual, less creative output
            )
        )
        if not response.text:
            print("Gemini API returned an empty response text.")
            return None

        parsed_output = json.loads(response.text)
        return parsed_output

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from Gemini API response: {e}")
        print(f"Raw response text (might be malformed JSON): {response.text}")
        return None
    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        return None