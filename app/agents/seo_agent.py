import os
from dotenv import load_dotenv

from app.services.sheets_service import (
    read_sheet,
    get_all_sheet_names,
)
from app.utils.llm import extract_seo_intent
from app.utils.response_generator import generate_natural_language_answer

load_dotenv()

SPREADSHEET_ID = os.getenv("SEO_SPREADSHEET_ID")


def seo_agent(query: str):
    """
    SEO Agent (Tier 2)
    Analyzes ALL sheets from Screaming Frog Google Sheets export.
    """

    if not SPREADSHEET_ID:
        return {
            "agent": "seo",
            "answer": "SEO spreadsheet is not configured.",
            "data": {}
        }

    intent = extract_seo_intent(query)
    issue = intent.get("issue_type")

    # 1️⃣ Load all sheets
    sheet_names = get_all_sheet_names(SPREADSHEET_ID)

    all_rows = []
    for sheet in sheet_names:
        rows = read_sheet(SPREADSHEET_ID, sheet)
        for r in rows:
            r["_sheet"] = sheet  # trace source sheet
        all_rows.extend(rows)

    # 2️⃣ Apply SEO rules
    results = []

    for row in all_rows:
        content_type = row.get("Content Type", "")

        # Only evaluate HTML pages
        if not content_type.startswith("text/html"):
            continue

        if issue == "missing_meta" and not row.get("Meta Description 1"):
            results.append(row)

        elif issue == "low_word_count":
            try:
                if int(row.get("Word Count", 0)) < 300:
                    results.append(row)
            except ValueError:
                pass

        elif issue == "missing_h1" and not row.get("H1-1"):
            results.append(row)

        elif issue == "error_pages" and str(row.get("Status Code", "")).startswith(("4", "5")):
            results.append(row)

        elif issue == "missing_canonical" and not row.get("Canonical Link Element 1"):
            results.append(row)

    structured_result = {
        "issue_type": issue,
        "count": len(results),
        "sample_urls": [row.get("Address") for row in results[:8]],
        "sheets_analyzed": len(sheet_names)
    }


    answer = generate_natural_language_answer(
        agent="seo",
        query=query,
        result=structured_result
    )

    return {
        "agent": "seo",
        "answer": answer,
        "data": structured_result
    }
