import os
def get_file_content(working_directory, file_path):
    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_abs_path.startswith(working_abs_path):
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_abs_path):
        return f"Error: File not found or is not a regular file: '{file_path}'"


    max_chars = 10000
    contents = ''
    truncated = False
    try:
        with open(target_abs_path, "r", encoding='utf-8') as file:
            for line in file:
                if len(contents) + len(line) >= max_chars:
                    remaning = max_chars - len(contents)
                    contents += line[:remaning]
                    truncated = True
                    break
                contents += line
        if truncated:
            contents = contents.rstrip() + f'[...File "{file_path}" truncated at 10000 characters]'

    except Exception as e:
        return f'Error reading file: {e}'
    

    return contents

