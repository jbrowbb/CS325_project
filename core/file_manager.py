import os
import json

def ensure_directory_exists(path):
    """Ensures that the specified directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)

def save_text_file(path, content):
    """Saves text content to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to: {path}")
        return True
    except IOError as e:
        print(f"Error saving text file to {path}: {e}")
        return False

def load_urls_from_file(path):
    """Loads URLs from a text file, one per line."""
    urls = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls, None # Return list of URLs and no error
    except FileNotFoundError:
        return [], f"Error: File not found at {path}"
    except Exception as e:
        return [], f"Error loading URLs from {path}: {e}"

def save_json_file(path, data):
    """Saves a dictionary as a JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"JSON data saved to: {path}")
        return True
    except IOError as e:
        print(f"Error saving JSON file to {path}: {e}")
        return False