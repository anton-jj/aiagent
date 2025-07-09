from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

system_prompt = """
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
"""
model_name = 'gemini-2.0-flash-001'

available_functions = types.Tool(
function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
    ]
)
