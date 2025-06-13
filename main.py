import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.available_functions import available_functions
from functions.call_function import call_function

load_dotenv()
api_key: str = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

system_prompt: str = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
user_prompt: str = sys.argv[1]
verbose: bool = True if "--verbose" in sys.argv else False
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
iteration: int = 0

while iteration < 20:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
    except IndexError as ie:
        print(f"IndexError: {ie}")
        sys.exit(1)

    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.function_calls and len(response.function_calls) > 0:
        for function_call_part in response.function_calls:
            function_call_result: types.Content = call_function(
                function_call_part, verbose
            )
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Invalid function response.")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)
    else:
        print(f"Response: {response.text}")
        break

    iteration += 1

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
