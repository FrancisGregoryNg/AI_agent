import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
            )
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        if os.path.isdir(file_path_abs):
            return (
                f"Error: Cannot write to {file_path} as it is a directory "
            )
        if (
            os.path.commonpath([working_directory_abs, file_path_abs]) 
            != working_directory_abs
        ):
            return (
                f'Error: Cannot write to "{file_path}" as it is outside '
                'the permitted working directory'
            )

        def write_file(file: str, content: str) -> str:
            with open(file, "w") as f:
                file_content = f.write(content)
                return (
                    f'Successfully wrote to "{file_path}" ' 
                    f'({len(content)} characters written)'
                )

        return write_file(file_path_abs, content)
        
    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write a new file or overwrite an existing file in a specified directory with a given file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to where the file is lcoated, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The text which will be written into the file",
                },
            },
        },
    },
}