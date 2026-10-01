import os

# Maximum characters we will read of a file.
MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        target_file_valid = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not target_file_valid:
            return f'Error: Cannot read "{file_path}" as it is outside of the working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        content = ""
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content


    except Exception as e:
        return f'Error: unexpected exception {e}'
