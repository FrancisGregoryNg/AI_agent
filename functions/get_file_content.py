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