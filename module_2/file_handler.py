# Input: Content and file path for writing; or file path for reading
# Output: Writes content to a file; returns content from a file

import os

class FileHandler:
    def __init__(self):
        pass

    def write_text_to_file(self, file_path: str, content: str) -> bool:
        try:
            # Ensure the directory exists
            output_dir = os.path.dirname(file_path)

            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)     # makes directory if does not exist
                print(f"Created directory: {output_dir}")

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        except IOError as e:
            print(f"Error writing to file '{file_path}': {str(e)}")
            return False
        

    def read_text_from_file(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: File not found at '{file_path}'"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        
        except IOError as e:
            return f"Error reading from file '{file_path}': {str(e)}"