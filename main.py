# main.py

from agents.nlu_agent import parse_event_prompt
from agents.event_scheduler import generate_feasible_slots
from agents.location_finder import find_places
import json

def orchestrate(user_input):
    # Step 1: Parse user input with NLU agent
    parsed = parse_event_prompt(user_input)
    
    # Defensive check: If parsing failed or empty response
    if not parsed or "error" in parsed:
        return {"status": "fail", "message": "NLU parsing failed."}
    
    # Extract fields safely
    event_name = parsed.get("event_name", "Unknown Event")
    duration_hours = parsed.get("duration_hours", 1)
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")
    location = parsed.get("location", "")

    # Step 2: Validate essential fields
    if not start_date or not end_date:
        return {"status": "fail", "message": "Missing dates in NLU output."}

    # Step 3: Generate feasible time slots
    slots = generate_feasible_slots(start_date, end_date, duration_hours)
    
    # Step 4: Find locations nearby
    places = find_places(query="restaurant", region=location)
    
    # Step 5: Combine and return final plan
    final_plan = {
        "status": "success",
        "event_name": event_name,
        "date_range": [start_date, end_date],
        "duration_hours": duration_hours,
        "feasible_slots": slots,
        "nearby_places": places
    }

    return final_plan


if __name__ == "__main__":
    user_prompt = "plan a casual lunch for 2 hours day after tomorrow around malad"
    result = orchestrate(user_prompt)
    
    print("----- Final Planner Output -----")
    print(json.dumps(result, indent=2))
