from datetime import date, datetime, timedelta

def resolve_date(spec: str) -> date:
    """
    Convert:
    today
    tomorrow
    yesterday
    +N
    -N
    YYYY-MM-DD
    into a datetime.date.
    """
    today = date.today()

    if spec == "today":
        return today

    if spec == "tomorrow":
        return today + timedelta(days=1)

    if spec == "yesterday":
        return today - timedelta(days=1)

    if spec.startswith("+") or spec.startswith("-"):
        try:
            offset = int(spec)
            return today + timedelta(days=offset)
        except ValueError:
            pass

    try:
        return datetime.strptime(spec, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date specification: {spec}")
