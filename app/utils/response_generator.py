from app.utils.llm import call_llm


def generate_natural_language_answer(agent: str, query: str, result: dict) -> str:
    """
    Converts structured agent output into a clear, human-readable answer.

    This function ensures:
    - No raw JSON is exposed to the user
    - Responses are concise, actionable, and natural
    - Safe fallbacks when no issues are found
    """

    issue_type = result.get("issue_type")
    count = result.get("count", 0)
    sample_urls = result.get("sample_urls", [])

    # ✅ Deterministic fallback when no issues are found
    if count == 0:
        return (
            "I analyzed your website and did not find any pages affected by this SEO issue. "
            "This suggests that your site is currently healthy in this area."
        )

    # Limit URLs for prompt safety
    example_urls = sample_urls[:5]

    prompt = f"""
You are a professional SEO consultant.

User question:
"{query}"

SEO analysis summary:
- Issue detected: {issue_type}
- Total affected pages: {count}
- Example affected URLs: {example_urls}

Explain clearly in plain English:
1. What this SEO issue means
2. Why it matters for search visibility
3. What actions should be taken to fix it

Keep the explanation concise, professional, and actionable.
Do NOT mention spreadsheets, APIs, code, or JSON.
"""

    try:
        return call_llm(prompt)
    except Exception:
        return (
            "I analyzed the SEO data and identified issues that may impact search performance, "
            "but I could not generate a detailed explanation at this moment."
        )
