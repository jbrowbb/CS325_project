from bs4 import BeautifulSoup
import requests

class DownLoadHelper:
    def __init__(self):
        pass

    def get_job(self,url):
        try:
            response = requests.get(url)
            html_content = response.text
        
            job = Job(url)
            job.set_html(html_content)
            job.parse()
            job_text = job.text.strip()
            

            return job_text
    
        except Exception as e:
            return f"Error occurred: {str(e)}"
        