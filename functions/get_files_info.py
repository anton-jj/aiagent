import os 

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."

    path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(path)
    working_dir_abs = os.path.abspath(working_directory)
    print(abs_path)

    if not abs_path.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    result_lines = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        is_dir = os.path.isdir(item_path)
        file_size = os.path.getsize(item_path)

        result_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(result_lines)
    




