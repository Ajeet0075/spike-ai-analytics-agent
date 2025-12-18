import os
from openai import OpenAI
from dotenv import load_dotenv

import json
import re

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



def extract_analytics_intent(query: str) -> dict:
    """
    Uses LiteLLM to extract GA4 intent in structured JSON.
    Falls back safely on any failure.
    """

    prompt = f"""
You are an analytics query parser.

Convert the user query into STRICT JSON with this schema:
{{
  "metrics": [string],
  "dimensions": [string],
  "days": number
}}

Rules:
- Use GA4 metric names only
- Use GA4 dimension names only
- If time range not mentioned, default to 14 days
- Output ONLY valid JSON, no explanation

User query:
"{query}"
"""

    try:
        raw = call_llm(prompt)

        # Extract JSON safely even if model adds text
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        intent = json.loads(match.group())

        return intent

    except Exception:
        # Safe deterministic fallback
        return {
            "metrics": ["screenPageViews", "activeUsers"],
            "dimensions": ["date"],
            "days": 14,
        }
    
def extract_seo_intent(query: str) -> dict:
    """
    Deterministic SEO intent extraction with LLM-safe fallback.
    """

    q = query.lower()

    if "meta" in q:
        return {"issue_type": "missing_meta"}

    if "word" in q or "thin" in q:
        return {"issue_type": "low_word_count"}

    if "index" in q:
        return {"issue_type": "non_indexable"}

    if "error" in q or "4xx" in q or "5xx" in q:
        return {"issue_type": "error_pages"}

    if "h1" in q:
        return {"issue_type": "missing_h1"}

    # Optional LLM usage (non-blocking, best-effort)
    try:
        response = call_llm(query).lower()
        if "meta" in response:
            return {"issue_type": "missing_meta"}
    except Exception:
        pass

    return {"issue_type": "unknown"}
