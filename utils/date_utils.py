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

# if __name__ == "__main__":
#     print(validate_date_format("2025-07-10"))  # True
#     print(validate_date_format("2025-13-10"))  # False

#     slots = generate_feasible_slots("2025-07-10", "2025-07-11", 2)
#     for slot in slots:
#         print(slot)

