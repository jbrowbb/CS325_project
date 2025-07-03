import re

def clean_filename(text):
    """
    Cleans text to be suitable for a filename by replacing invalid characters
    and limiting length.
    """
    # Replace non-alphanumeric (except underscore, hyphen, period, space) with underscore
    cleaned_text = re.sub(r'[^\w\s.-]', '', text)
    # Replace spaces with underscores and remove leading/trailing underscores
    cleaned_text = re.sub(r'\s+', '_', cleaned_text).strip('_')
    # Limit to a reasonable length to avoid path issues
    return cleaned_text[:100] # Limit length for safety