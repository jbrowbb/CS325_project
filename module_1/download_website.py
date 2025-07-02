from module_1.DownloadHelper import DownLoadHelper


class DownloadJob:
    def __init__(self):
        pass

    def download_tex_from_file(self,url,index):
        try:
            
            job_downloader = DownLoadHelper()
            job_content = job_downloader.get_article(url)
      
    
            # Write content to a file
            output_path = f"Job/General/Job_{index+1}.txt" #which position want to save
            with open(output_path, 'w') as job_file:
                job_file.write(job_content)
            print(f"Job {index+1} saved to file.")
        except Exception as e:
            print(f"Error occurred: {str(e)}")