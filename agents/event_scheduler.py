from utils.date_utils import validate_date_format
from utils.logger import logger
from datetime import datetime, timedelta

def generate_feasible_slots(start_date, end_date, duration_hours):
    slots = []
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    work_start = 11
    work_end = 22

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

def schedule_event(event_name, start_date, end_date, duration_hours):
    logger.info(f'Scheduling event : {event_name} from {start_date} to {end_date} for {duration_hours} hours')

    if not (validate_date_format(start_date)) and (validate_date_format(end_date)):
        logger.error('Invalid date format. Expected YYYY-MM-DD')
        return {'error' : 'Invalid date format'}
    
    if duration_hours <= 0:
        logger.error("Duration must be positive.")
        return {"error": "Duration must be positive"}
    
    from datetime import datetime
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    if start > end:
        logger.error("Start date cannot be after end date.")
        return {"error": "Start date after end date"}
    
    slots = generate_feasible_slots(start_date, end_date, duration_hours)

    result = {
        'event' : event_name,
        'slots' : slots
    }

    logger.info(f"Generated {len(slots)} slots for event '{event_name}'")
    return result

# if __name__ == '__main__':
#     output = schedule_event("AI Workshop", "2025-07-10", "2025-07-10", 2)
#     print(output)

