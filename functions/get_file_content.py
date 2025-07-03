import os
def get_file_content(working_directory, file_path):
    workining_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.abspath(file_path)
    if not target_abs_path.startswith(workining_abs_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_abs_path):
        return f"Error: File not found or is not a regular file: '{file_path}'"

    abs_path = os.path.join(workining_abs_path, target_abs_path)
    max_chars = 1000

    contents = ''
    truncated = False
    with open(abs_path, "r") as file:
        for line in file:
            if len(contents) + len(line) >= max_chars:
                remaning = max_chars - len(contents)
                contents += line[:remaning]
                truncated = True
                break
            contents += line
    if truncated:
        contents = contents.rstrip() + f'[...File "{file_path}" truncated at 10000 characters]'

    return contents

