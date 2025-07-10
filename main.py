import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, model_name, available_functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file
import sys

def main():
    load_dotenv()
    args = sys.argv[1:]
    verbose = "--verbose" in sys.argv

    if not args:
        print("Ai needs a argument")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client =  genai.Client(api_key=api_key)
    user_prompt = " ".join(args)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print("User prompt: ", user_prompt)

    create_content(client, messages, verbose)

def create_content(client, messages, verbose):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )

    if response.function_calls:
        for function in response.function_calls:
            result = call_function(function, verbose)
            if not hasattr(result.parts[0], "function_response") or \
                not hasattr(result.parts[0].function_response, "response"):
                raise RuntimeError("Function call did not return a valid response.")
            response_data = result.parts[0].function_response.response
            if "result" in response_data:
                    print(response_data["result"])
            elif "error" in response_data:
                    print(response_data["error"])
            else:
                print("Unknown response structure:", response_data)
    # LOG THE RAW RESPONSE!
    else:
        print("DEBUG: Model did not return a function call.")
        print("DEBUG FULL RESPONSE:", response)
        # Or, if you want just the plain text response parts:
        if hasattr(response, "candidates"):
            for cand in response.candidates:
                if cand.content and cand.content.parts:
                    for p in cand.content.parts:
                        print("DEBUG PART:", p)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    # Add this:
    if function_name == "get_files_info" and "directory" not in args:
        args["directory"] = "."
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"->Calling function: {function_call_part.name}({args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
    try:
        args["working_directory"] = "./calculator"
        result = function_map[function_name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": str(e)}
            )
        ]
    )

if __name__ == "__main__":
    main()
