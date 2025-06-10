import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key: str = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

system_prompt: str = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
user_prompt: str = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
except IndexError as ie:
    print(f"IndexError: {ie}")
    sys.exit(1)


print(f"Response: {response.text}")

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
