import os
def write_file(working_directory, file_path, content):
    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_abs_path.startswith(working_abs_path):
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_abs_path):
        with open (target_abs_path, "w") as file:
            file.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    pass
