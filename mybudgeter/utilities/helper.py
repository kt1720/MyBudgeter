from datetime import datetime, timedelta

def calculation_query(type, categories=None, months=None, years=None):
    """Prepare conditions and values for the WHERE clause used in total and average in the User class"""
    conditions = []
    values = []

    if categories:
        if isinstance(categories, str):
            categories = [categories]
        placeholders = ', '.join('?' for _ in categories)
        conditions.append(f"category IN ({placeholders})")
        values.extend(categories)

    if months:
        if not isinstance(months, list):
            months = [months]
        if type == "transactions":
            month_placeholders = ', '.join('?' for _ in months)
            conditions.append(f"strftime('%m', trans_date) IN ({month_placeholders})")
            values.extend(str(month) for month in months)
        elif type == "budget":
            month_placeholders = ', '.join('?' for _ in months)
            conditions.append(f"month IN ({month_placeholders})")
            values.extend(months)

    if years:
        if not isinstance(years, list):
            years = [years]
        if type == "transactions":
            year_placeholders = ', '.join('?' for _ in years)
            conditions.append(f"strftime('%Y', trans_date) IN ({year_placeholders})")
            values.extend(str(year) for year in years)
        elif type == "budget":
            year_placeholders = ', '.join('?' for _ in years)
            conditions.append(f"year IN ({year_placeholders})")
            values.extend(years)
    # Add WHERE clause if conditions are present
    where_clause = " AND ".join(conditions)
    return where_clause, values

def spending_query(calculate_category=True, order_by="DESC"):
    """
    Find the spending based on the provided input.
    - If calculate_category is True, find the highest/lowest spending category in general.
    - If calculate_category is False, find the highest/lowest spending month in the current year.
    - order_by: "DESC" for highest spending, "ASC" for lowest spending
    """
    query_type = "category" if calculate_category else "strftime('%m', trans_date) as month"
    order = f"ORDER BY SUM(amount) {order_by}"

    current_year = datetime.now().year
    query = f"SELECT {query_type}, SUM(amount) FROM transactions"
    conditions = f" WHERE strftime('%Y', trans_date) = ?" if not calculate_category else ""
    query += f"{conditions} GROUP BY category {order} LIMIT 1" if calculate_category else f"{conditions} GROUP BY month {order} LIMIT 1"

    values = (str(current_year),) if not calculate_category else ()

    return query, values

def linechart_query(type):
    """Build query for the linechart function in the User class"""
    # Get the current date
    end_date = datetime.now()
    # Calculate the start date (12 months ago)
    start_date = end_date - timedelta(days=365)
    # Format the dates for the SQLite query
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    if type == "transactions":
        query = f"SELECT strftime('%Y-%m', trans_date) AS month, SUM(amount) FROM {type} WHERE trans_date BETWEEN '{start_date_str}' AND '{end_date_str}' GROUP BY strftime('%Y-%m', trans_date) ORDER BY month"
    else:
        query = f"SELECT printf('%d-%02d', year, month) AS month, SUM(amount) FROM {type} WHERE printf('%d-%02d', year, month) BETWEEN '{start_date_str}' AND '{end_date_str}' GROUP BY year, month ORDER BY month"
    return query