from google import genai
import traceback

from llm.config import GEMINI_API_KEY, GEMINI_MODEL
from llm.prompt import SYSTEM_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)


def generate(user_prompt: str):

    try:

        print("GENERATOR START")

        full_prompt = f"""
{SYSTEM_PROMPT}

{user_prompt}
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt,
        )

        print("GENERATOR END")

        return response.text

    except Exception:
        traceback.print_exc()
        raise