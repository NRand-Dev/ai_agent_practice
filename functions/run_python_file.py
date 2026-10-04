import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a function in a specified file_path relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File_path to python module, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "arguments passed to function being called.",
                }
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absoute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absoute_path, file_path))
        target_file_valid = os.path.commonpath([absoute_path, target_file]) == absoute_path

        if not target_file_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'


        # Command a subprocess to run the file
        command = ["python", target_file]
        if args:
            command.extend(args)

        completed_process_object = subprocess.run(command, capture_output=True, text=True, cwd=absoute_path, timeout=30.0)

        if not completed_process_object.returncode == 0:
            return f'Process exited with code {completed_process_object.returncode}'
        if not completed_process_object.stderr and not completed_process_object.stdout:
            return f'No output produced'
        std_out_string = f"STDOUT: {completed_process_object.stdout}"
        std_err_string = f'STDERR:: {completed_process_object.stderr}'

        return std_out_string + std_err_string





    except Exception as e:
        return f'Error: Unexpected error {e}'
