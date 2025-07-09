import os
import subprocess

from google.genai import types
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        if args is None:
            args = []

        working_abs_path = os.path.abspath(working_directory)
        target_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_abs_path.startswith(working_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_abs_path):
            return f'Error: File "{file_path}" not found.'

        if not target_abs_path.endswith(".py"):
            return f'Error: File "{file_path}" is not a Python file.'

        command = ["python3", target_abs_path] + args

        res = subprocess.run(
           command,
                              capture_output=True,
                              text=True,
                              timeout=30,
                              cwd=working_abs_path
        )
        stdout = res.stdout.strip()
        stderr = res.stderr.strip()

        output = []

        if stdout:
            output.append("STDOUT:\n" + stdout)
        if stderr:
            output.append("STDERR:\n" + stderr)
        if res.returncode != 0:
            output.append(f"Process exited with code {res.returncode}")

        if not output:
            return "No output produced."

        return "\n\n".join(output)
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.strip() if e.stdout else ""
        stderr = e.stderr.strip() if e.stderr else ""
        output = ["Process timed out after 30 seconds."]

        if stdout:
            output.append("STDOUT:\n" + stdout)
        if stderr:
            output.append("STDERR:\n" + stderr)
        return "\n\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
