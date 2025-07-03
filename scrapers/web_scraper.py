import requests
from bs4 import BeautifulSoup
import re

def scrape_website_to_plain_text(url):
    """
    Scrapes a given URL and returns the main text content,
    attempting to filter out common irrelevant elements.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        main_content_div = soup.find(['article', 'main', 'div', 'section'], class_=re.compile(r'job|description|content|body|post', re.I))

        if not main_content_div:
            main_content_div = soup.find('body')

        if not main_content_div:
            return None, "Could not find a discernible main content area on the page."

        text_elements = main_content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'span', 'div'])
        plain_text = []
        for element in text_elements:
            cleaned_text = re.sub(r'\s+', ' ', element.get_text(separator=" ", strip=True)).strip()
            if cleaned_text:
                plain_text.append(cleaned_text)

        full_text = "\n\n".join(plain_text)
        full_text = re.sub(r'\n\s*\n', '\n\n', full_text)
        full_text = re.sub(r'[ \t]+', ' ', full_text)
        full_text = full_text.strip()

        if not full_text:
            return None, "No significant text content extracted from the identified area."

        return full_text, None

    except requests.exceptions.HTTPError as e:
        return None, f"HTTP Error {e.response.status_code}: {e.response.reason} for {url}"
    except requests.exceptions.ConnectionError as e:
        return None, f"Connection Error: {e} for {url}. Check internet connection or URL."
    except requests.exceptions.Timeout as e:
        return None, f"Timeout Error: Request timed out for {url}."
    except requests.exceptions.RequestException as e:
        return None, f"An ambiguous request error occurred: {e} for {url}."
    except Exception as e:
        return None, f"An unexpected error occurred during web scraping: {e} for {url}."