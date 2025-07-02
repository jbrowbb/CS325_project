# Generates the summaries
import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiGenerateResume:
    # Load environment variables from .env file
    load_dotenv()

    # Configure generativeai with API key from environment variables
    genai.configure(api_key=os.environ["API_KEY"])

    #generate job titles based on skills and previous jobs
    def generate_resume(self,resume_content):
        model = genai.GenerativeModel('gemini-pro') #model
        #input your instruction
        response = model.generate_content(f"Can you look at the past job experiences and skills to find out some job titles i should look at and locations \"{resume_content}\"")
    
        return response.text
        
    #save the summary to the txt file
    def save_resume(self,title, concise_resume):
        output_path = f"Resume/summary.txt" # which location want to output
        with open(output_path, "w") as file:
            file.write(f"Concise Resume:\n{concise_resume}")
        print(f"Resume summary saved to file.")



class GeminiGenerateJobs:
    # Load environment variables from .env file
    load_dotenv()

    # Configure generativeai with API key from environment variables
    #genai.configure(api_key=os.environ["API_KEY"])
    def configure_genai_with_api_key():
     #Check if API key is available
        api_key = os.getenv("API_KEY")
        if api_key:
            try:
                # Configure generativeai with API key
                genai.configure(api_key=os.environ["API_KEY"])
                print("GenerativeAI configured successfully.")
                return True
            except KeyError:
                print("API_KEY environment variable not found.")
                return False
            except Exception as e:
                print(f"Error configuring GenerativeAI: {str(e)}")
                return False
        else:
            print("API_KEY environment variable not really found.")
            return False
        
    #generate the summary of the article
    def generate_concise_article(self,job_content):
        model = genai.GenerativeModel('gemini-pro') #model
        #input your instruction
        response = model.generate_content(f"Please summarize the job desctiption with skill needed, what the job is, location, and pay. The article is \"{job_content}\"")
    
        return response.text
    
    #generate the title of the article
    def generate_spicy_title(self,job_text):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Please take the job title. The title is \"{job_text}\"")
    
        return response.text
        
    #save the summary and title to the txt file
    def save_article(self,title, concise_job,index):
        output_path = f"Jobs/Summarized/summary_{index+1}.txt" # which location want to output
        with open(output_path, "w") as file:
            file.write(f"Title: {title}\n\n")
            file.write(f"Concise Job:\n{concise_job}")
        print(f"Summary {index+1} saved to file.")
