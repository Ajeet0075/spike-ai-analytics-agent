from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension,
)
from google.oauth2 import service_account


def run_ga4_report(
    property_id: str,
    metrics: list[str],
    dimensions: list[str],
    start_date: str,
    end_date: str,
):
    """
    Executes a GA4 Data API report query.
    """

    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json"
    )

    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in dimensions],
    )

    response = client.run_report(request)

    results = []

    for row in response.rows:
        record = {}

        for i, dim in enumerate(dimensions):
            record[dim] = row.dimension_values[i].value

        for i, met in enumerate(metrics):
            record[met] = row.metric_values[i].value

        results.append(record)

    return results
