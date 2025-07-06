import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, model_name, available_functions
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

    if verbose:
        print("Prompt tokens:",response.usage_metadata.prompt_token_count)
        print("Response tokens:",response.usage_metadata.candidates_token_count)

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()

