import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        if not os.path.isfile(file_path_abs):
            return (
                f'Error: "{file_path}" does not exist or is not a regular file'
            )
        
        if file_path_abs[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        if (
            os.path.commonpath([working_directory_abs, file_path_abs])
            != working_directory_abs
        ):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the '
                'permitted working directory'
            )

        command = ["python", file_path_abs]
        if args:
            command.extend(args)

        result = subprocess.run(
                command, 
                capture_output=True, 
                timeout= 30, 
                text=True,
            )

        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output_string += "No output produced"
        if result.stdout:
            output_string += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output_string += f"STDERR:\n{result.stderr}"

        return output_string
    
    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python script in a specified directory with a given file path and additional arguments (if any)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to where the file is lcoated, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "string",
                    "description": "Optional additional arguments to run the Python script",
                },
            },
        },
    },
}