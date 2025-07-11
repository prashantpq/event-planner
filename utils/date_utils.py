from datetime import datetime, timedelta

def validate_date_format(date_str):
    """
    validates that the date string is in 'YYYY-MM-DD' format.
    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

import dateparser

def parse_relative_date(relative_date_str, reference_date=None):
    """
    Converts 'day after tomorrow' to 'YYYY-MM-DD' format based on reference_date.
    """
    if reference_date is None:
        reference_date = datetime.today()
    parsed_date = dateparser.parse(relative_date_str, settings={'RELATIVE_BASE': reference_date})
    if parsed_date:
        return parsed_date.strftime("%Y-%m-%d")
    else:
        return None
    



