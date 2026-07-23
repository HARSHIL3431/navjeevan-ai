from datetime import datetime

def validate_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        if dt > datetime.now():
            raise ValueError("Sowing date cannot be in the future")
        return date_str
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("Invalid date format. Expected YYYY-MM-DD")
        raise e
