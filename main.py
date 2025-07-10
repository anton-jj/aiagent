import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, model_name, available_functions, MAX_ITERS
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

    if verbose:
        print("User prompt: ", user_prompt)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = create_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def create_content(client, messages, verbose):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )

    if hasattr(response, "candidates") and response.candidates:
        for cand in response.candidates:
            if cand.content and cand.content.parts:
                for p in cand.content.parts:
                    print("DEBUG PART:", p)
                    if hasattr(p, "function_call") and p.function_call is not None:
                        function_call_part = p.function_call
                        result = call_function(function_call_part, verbose)
                        if hasattr(result.parts[0], "function_response") and hasattr(result.parts[0].function_response, "response"):
                            response_data = result.parts[0].function_response.response
                        if "result" in response_data:
                            messages.append(types.Content(role="tool", parts=[types.Part(text=response_data["result"])]))
                            print(response_data["result"])
                        elif "error" in response_data:
                            messages.append(types.Content(role="tool", parts=[types.Part(text=f"Error: {response_data['error']}")]))
                            print(f"Error: {response_data['error']}")
                        else:
                            print("Unknown response structure:", response_data)
                    else:
                        print(f"Function call did not return valid response: {p}")

            elif hasattr(p, "text"):
                print("Model Response:", p.text)
                messages.append(types.Content(role="assistant", parts=[types.Part(text=p.text)]))
                return p.text

            else:
                print("No function call or text found in part:", p)

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
