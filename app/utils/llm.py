import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def call_llm(prompt: str) -> str:
    """
    Calls LiteLLM proxy (Gemini model) for reasoning.
    """

    api_key = os.getenv("LITELLM_API_KEY")
    base_url = os.getenv("LITELLM_BASE_URL")
    model = os.getenv("LITELLM_MODEL", "gemini-1.5-flash")

    if not api_key or not base_url:
        raise RuntimeError("LiteLLM environment variables not set")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content
