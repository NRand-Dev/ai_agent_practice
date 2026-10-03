import os


# Schema for LLM to describe functions it would like to call
# We do NOT pass working directory to the LLM, so that we can control that ourselves without any outside input.
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

# --- GET_FILES_INFO NOTES --- #

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
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        if target_dir_valid:
            # After filepath validation - SEE ABOVE
            # Iterate over the items in the target directory.
            # Contents = what is in the target_dir
            contents = []
            # need to use the os method to the get absolute file path, not just the string value
            for item in os.listdir(target_dir):
                file_path = os.path.join(target_dir, item)
                name = item
                size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                new_string = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
                contents.append(new_string)

            return "\n".join(contents)

    except Exception as e:
        return f'Error: unexpected error as {e}'
