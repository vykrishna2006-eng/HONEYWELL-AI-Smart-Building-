import requests
import traceback

from llm.config import OLLAMA_HOST, OLLAMA_MODEL
from llm.prompt import SYSTEM_PROMPT


def generate(user_prompt: str) -> str:

    try:

        full_prompt = f"""
{SYSTEM_PROMPT}

{user_prompt}
"""

        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception:
        traceback.print_exc()
        raise