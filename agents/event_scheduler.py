from utils.date_utils import validate_date_format, generate_feasible_slots
from utils.logger import logger

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

if __name__ == '__main__':
    output = schedule_event("AI Workshop", "2025-07-10", "2025-07-12", 2)
    print(output)
