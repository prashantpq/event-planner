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

def generate_feasible_slots(start_date, end_date, duration_hours):
    slots = []
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    work_start = 9
    work_end = 18

    current_date = start
    while current_date <= end:
        slot_start = work_start
        while slot_start + duration_hours <= work_end:
            slot_end = slot_start + duration_hours
            slots.append({
                'date' : current_date.strftime('%Y-%m-%d'),
                'start_time' : f'{int(slot_start):02d}:00',
                'end_time' : f'{int(slot_end):02d}:00'
            })
            slot_start = slot_end
        current_date += timedelta(days=1)

    return slots

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
    
    


