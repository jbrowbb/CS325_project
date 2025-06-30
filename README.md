# Indeed Resume and Job Summarizer
This program streamlines job searching by leveraging the power of Gemini's AI. It begins by processing your PDF resume to extract key information. Gemini then identifies relevant job titles and locations, which are used to query Indeed.com. The program retrieves the top 5-10 results, scrapes their text, and uses Gemini's AI again to generate concise summaries of job descriptions, salary expectations, and required skills. This sophisticated tool significantly reduces the time and effort involved in finding suitable job opportunities. The entire process, from resume analysis to summarized job details, is powered by the advanced capabilities of Gemini's AI, providing a seamless and efficient job search experience.

# Features
* Extract text from PDF
* Saves the extracted content in a text file
* Uses Gemini's AI to help find job listings and locations
* Extracts content from HTML structured websites
* Uses Gemini's AI fetures to summarize job descriptions, locations, and pay

# Supported Websites
The program currently supports downloading content from the following job listing websites:

* Indeed.com

# Installation

1. Clone the repository
```bash
git clone https://github.com/jbrowbb/CS325_project.git
```

2. Navigate to the project directory
```bash
cd 'Indeed Project'
```

3. Initialize the conda environment with the provided `requirements.yaml` file
```bash
conda env create -f requirements.yaml
```

4. Activate the conda environment
```bash
conda activate job_matching_env
```