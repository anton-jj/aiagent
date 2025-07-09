import os
from google.genai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to write or overwrite",
            ),
            "Content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"

            )
        },
        required=["file_path", "Content"],
    ),
)
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
