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
def slot_generator_tool(start_date: str, end_date: str, duration_hours: int) -> dict:
    """
    Generate feasible time slots for the event based on date range and duration.
    Returns dict with key: feasible_slots.
    """
    slots = generate_feasible_slots(start_date, end_date, duration_hours)
    return {"feasible_slots": slots}

@tool
def location_finder_tool(location: str, query: str = "restaurant") -> dict:
    """
    Find nearby places based on location and query type.
    Returns dict with key: nearby_places.
    """
    places = find_places(query, location)
    return {"nearby_places": places}

@tool
def budget_estimator_tool(duration_hours: int = 3, number_of_people: int = 1, location: str = "unknown", feasible_slots: list = None, nearby_places: list = None) -> dict:
    """
    Estimate budget for the event based on duration, number of people, and location.
    Accepts optional feasible_slots and nearby_places to support flexible calling from agent.
    Returns dict with key: budget_estimate.
    """
    duration = duration_hours if duration_hours else 2

    budget = estimate_budget(duration, number_of_people, location)
    return {"budget_estimate": budget}
