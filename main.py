import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=sys.argv[1]
    )
except IndexError as ie:
    print(f"IndexError: {ie}")
    sys.exit(1)

print(f"""
    Response: {response.text}
    Prompt tokens: {response.usage_metadata.prompt_token_count}
    Response tokens: {response.usage_metadata.candidates_token_count}
""")
