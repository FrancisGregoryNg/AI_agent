import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        directory_abs = os.path.normpath(
            os.path.join(working_directory_abs, directory)
            )
        if not os.path.isdir(directory_abs):
            return f'Error: "{directory}" is not a directory'
        if (
            os.path.commonpath([working_directory_abs, directory_abs]) 
            != working_directory_abs
        ):
            return (
                f'Error: Cannot list "{directory}" as it is outside'
                " the permitted working directory"
            )

        files = os.listdir(directory_abs)

        def get_file_details(file: str) -> str:
            nonlocal directory_abs
            file_path = os.path.normpath(
                os.path.join(directory_abs, file)
            )
            file_size = os.path.getsize(file_path)
            file_is_dir = os.path.isdir(file_path)
            return f"{file}: file_size={file_size}, is_dir={file_is_dir}"

        return '\n'.join(map(get_file_details, files))
        
    
    except Exception as e:
        return f'Error: {e}'