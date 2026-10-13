import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        directory_abs = os.path.normpath(os.path.join(working_directory_abs, directory))
        if not os.path.isdir(directory_abs):
            return f'Error: "{directory}" is not a directory'
        if os.path.commonpath([working_directory_abs, directory_abs]) != working_directory_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {e}'