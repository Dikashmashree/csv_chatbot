import pandas as pd


def execute_query(df: pd.DataFrame, structured_query: dict) -> list:
    """
    Applies filters, sorting, and limit from a structured query dict
    to a DataFrame and returns results as a list of dicts.
    """
    results = df.copy()

    filters = structured_query.get("filters", {})
    sort_by = structured_query.get("sort_by")
    order = structured_query.get("order", "desc")
    limit = structured_query.get("limit", 5)

    for column, value in filters.items():
        if column in results.columns and value:
            results = results[
                results[column].astype(str).str.contains(str(value), case=False, na=False)
            ]

    if sort_by and sort_by in results.columns:
        ascending = (order == "asc")
        results = results.sort_values(by=sort_by, ascending=ascending)
    return results.head(limit).to_dict(orient="records")