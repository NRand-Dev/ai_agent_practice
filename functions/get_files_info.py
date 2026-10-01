import os

# NOTE: get_files_info() should ALWAYS return a string. If errors can be raised, we need to catch those and return error messages as strings.
# This allows the LLM to handle errors gracefully by always having a statement to print.

# Directory is a file path relative to the working_directory.
# LLM - will define which directories it wants to scan. (Directory)
# USER - Sets (working_directory). Allows us to limit the scope of the directories and files the LLM can view.
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(absolute_path, directory))

        target_dir_valid = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        # Target_dir not valid
        if not target_dir_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if directory is a directory
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        if target_dir_valid:
            return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f'Error: unexpected error as {e}'
