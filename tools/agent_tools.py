from langchain.tools import tool
from agents.nlu_agent import parse_event_prompt
from agents.event_scheduler import generate_feasible_slots
from agents.location_finder import find_places
from agents.budget_estimator import estimate_budget

@tool
def nlu_tool(user_input: str) -> dict:
    """
    NLU tool to parse user input and extract event details.
    Returns a dict with keys: event_name, duration_hours, start_date, end_date, location, number_of_people.
    """
    return parse_event_prompt(user_input)

@tool
def slot_generator_tool(start_date: str, end_date: str = None, duration_hours: int = 1) -> dict:
    """
    Generate feasible time slots for the event based on date range and duration.
    Returns dict with key: feasible_slots.
    """
    if end_date is None:
        end_date = start_date
    slots = generate_feasible_slots(start_date, end_date, duration_hours)
    return {"feasible_slots": slots}



@tool
def slot_selection_tool(event_name: str, feasible_slots: list) -> dict:
    """
    Selects the best slot based on event context.

    Rules:
    - Dates prefer evening slots (17:00 onwards).
    - Lunch prefers 12:00-15:00 slots.
    - Dinner prefers 19:00 onwards (if available).
    - Default: returns first slot.
    """
    selected = feasible_slots[0]  

    if feasible_slots:
        if "date" in event_name.lower():
            # Prefer evening slots (17:00 onwards)
            evening_slots = [slot for slot in feasible_slots if int(slot['start_time'].split(":")[0]) >= 17]
            if evening_slots:
                selected = evening_slots[0]
        elif "lunch" in event_name.lower():
            lunch_slots = [slot for slot in feasible_slots if 12 <= int(slot['start_time'].split(":")[0]) < 15]
            if lunch_slots:
                selected = lunch_slots[0]
        elif "dinner" in event_name.lower():
            dinner_slots = [slot for slot in feasible_slots if int(slot['start_time'].split(":")[0]) >= 19]
            if dinner_slots:
                selected = dinner_slots[0]

    return {"selected_slot": selected}


@tool
def location_finder_tool(location: str, query_type: str = "restaurant") -> dict:
    """
    Find nearby places based on location and query type.
    Returns dict with key: nearby_places.
    """
    places = find_places(query_type, location)
    return {"nearby_places": places}


@tool
def budget_estimator_tool(number_of_people: int = 1, location: str = "unknown", feasible_slots: list = None, nearby_places: list = None) -> dict:
    """
    Estimate budget for the event based on duration, number of people, and location.
    Accepts optional feasible_slots and nearby_places to support flexible calling from agent.
    Returns dict with key: budget_estimate.
    """

    budget = estimate_budget(number_of_people, location)
    return {"budget_estimate": budget}
