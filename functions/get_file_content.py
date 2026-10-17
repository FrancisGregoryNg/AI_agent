import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
            )
        if not os.path.isfile(file_path_abs):
            return (
                f"Error: File not found or is not a regular file: "
                f'"{file_path}"'
            )
        if (
            os.path.commonpath([working_directory_abs, file_path_abs]) 
            != working_directory_abs
        ):
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                'the permitted working directory'
            )

        def read_file(file: str) -> str:
            with open(file, "r") as f:
                file_content = f.read(MAX_CHARS)
                if f.read(1):
                    file_content += (
                        f'[...File "{file}" truncated at {MAX_CHARS} '
                        'characters]'
                    )
                return file_content

        return read_file(file_path_abs)
        
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the contents of a file in a specified directory, limited by a global character limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to where the file is lcoated, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}