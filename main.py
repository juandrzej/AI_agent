import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key: str = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a given file in a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, overwriting what was that so far, creating a new file if it did not exist, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content which will be written to the given file.",
            ),
        },
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run the python program, relative to the working directory.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

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
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

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


if response.function_calls and len(response.function_calls) > 0:
    for func_call in response.function_calls:
        function_call_part = func_call
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(f"Response: {response.text}")

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
