from app.services.ga4_service import run_ga4_report
from app.utils.llm import extract_analytics_intent, call_llm


ALLOWED_METRICS = {
    "activeUsers",
    "totalUsers",
    "screenPageViews",
    "sessions",
}

ALLOWED_DIMENSIONS = {
    "date",
    "pagePath",
    "country",
    "deviceCategory",
}


def generate_nl_answer(query: str, result: dict) -> str:
    """
    Generate natural language analytics answer using LLM.
    """
    prompt = f"""
You are an analytics assistant.

User question:
"{query}"

Analytics result:
{result}

Write a clear, concise, natural language answer.
Explain insights in plain English.
Do NOT mention APIs, JSON, or code.
"""

    try:
        return call_llm(prompt)
    except Exception:
        return (
            "I analyzed the analytics data successfully, but could not generate "
            "a detailed explanation at this moment."
        )


def analytics_agent(query: str, property_id: str):
    """
    GA4 Analytics Agent (Tier 1)
    """

    intent = extract_analytics_intent(query)

    metrics = intent.get("metrics", [])
    dimensions = intent.get("dimensions", [])
    days = intent.get("days", 14)

    start_date = f"{days}daysAgo"
    end_date = "today"

    metrics = [m for m in metrics if m in ALLOWED_METRICS]
    dimensions = [d for d in dimensions if d in ALLOWED_DIMENSIONS]

    if not metrics:
        return {
            "agent": "analytics",
            "answer": "I could not identify valid Google Analytics metrics from your query.",
            "data": {
                "status": "failed",
                "reason": "No valid GA4 metrics inferred",
                "llm_intent": intent
            }
        }

    try:
        rows = run_ga4_report(
            property_id=property_id,
            metrics=metrics,
            dimensions=dimensions,
            start_date=start_date,
            end_date=end_date,
        )

        structured_result = {
            "metrics": metrics,
            "dimensions": dimensions,
            "date_range": {
                "start": start_date,
                "end": end_date,
            },
            "row_count": len(rows),
            "sample_rows": rows[:10]
        }

        # ✅ IMPORTANT FIX
        if len(rows) == 0:
            answer = (
                f"I checked your Google Analytics data for the last {days} days, "
                "but there is currently no recorded traffic available. "
                "Once your website or app starts receiving users, "
                "this agent will provide daily page views and user trends."
            )
        else:
            answer = generate_nl_answer(query, structured_result)

        return {
            "agent": "analytics",
            "answer": answer,
            "data": structured_result
        }

    except Exception as e:
        return {
            "agent": "analytics",
            "answer": (
                "I attempted to fetch analytics data, but the analytics "
                "property is not accessible or not fully configured."
            ),
            "data": {
                "status": "failed",
                "reason": "GA4 not configured or inaccessible",
                "details": str(e),
                "llm_intent": intent,
                "next_step": "Add credentials.json and a valid GA4 propertyId"
            }
        }
