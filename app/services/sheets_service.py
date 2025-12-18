from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_sheets_service():
    """
    Initialize and return Google Sheets API service.
    """
    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

    return build("sheets", "v4", credentials=credentials)


def get_all_sheet_names(spreadsheet_id: str) -> list[str]:
    """
    Fetch all sheet (tab) names from a spreadsheet.
    """
    service = get_sheets_service()

    spreadsheet = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id
    ).execute()

    return [
        sheet["properties"]["title"]
        for sheet in spreadsheet.get("sheets", [])
    ]


def read_sheet(spreadsheet_id: str, sheet_name: str) -> list[dict]:
    """
    Read all rows from a specific sheet and return as list of dicts.
    """
    service = get_sheets_service()

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_name
    ).execute()

    values = result.get("values", [])
    if not values:
        return []

    headers = values[0]
    rows = values[1:]

    data = []
    for row in rows:
        record = {
            headers[i]: row[i] if i < len(row) else ""
            for i in range(len(headers))
        }
        data.append(record)

    return data
