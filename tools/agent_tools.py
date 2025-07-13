# tools/agent_tools.py

from langchain.tools import tool
from agents.nlu_agent import parse_event_prompt
from agents.location_finder import find_places
from agents.event_scheduler import generate_feasible_slots
from agents.budget_estimator import estimate_budget

@tool
def nlu_tool(user_input: str) -> dict:
    """
    Perform natural language understanding on user input to extract event details.

    Args:
        user_input (str): The user's input describing the event.

    Returns:
        dict: Parsed event details including event name, duration, location, etc.
    """
    return parse_event_prompt(user_input)

@tool
def location_finder_tool(location: str, query_type: str = "restaurant", brand_name: str = None) -> dict:
    """
    Find nearby places based on location, query type, and optional brand.

    Args:
        location (str): The region or place to search around.
        query_type (str): Type of place to search for (e.g. cafe, restaurant).
        brand_name (str, optional): Specific brand to search for.

    Returns:
        dict: Dictionary containing a list of nearby places with their details.
    """
    places = find_places(brand_name, query_type, location)
    return {"nearby_places": places}

@tool
def slot_generator_tool(start_date: str, end_date: str = None, duration_hours: int = 1) -> dict:
    """
    Generate feasible time slots for the event.

    Args:
        start_date (str): Start date for slot generation.
        end_date (str, optional): End date for slot generation. Defaults to start_date.
        duration_hours (int, optional): Duration of each slot in hours. Defaults to 1.

    Returns:
        dict: Dictionary containing a list of feasible slots with timings.
    """
    if end_date is None:
        end_date = start_date
    slots = generate_feasible_slots(start_date, end_date, duration_hours)
    return {"feasible_slots": slots}

@tool
def slot_selection_tool(event_name: str, feasible_slots: list) -> dict:
    """
    Select the most suitable slot based on event type.

    Args:
        event_name (str): The name of the event (e.g. lunch, dinner).
        feasible_slots (list): List of feasible slots.

    Returns:
        dict: Dictionary containing the selected slot.
    """
    selected = feasible_slots[0]
    if feasible_slots:
        if "date" in event_name.lower():
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
def budget_estimator_tool(number_of_people: int = 1, location: str = "unknown") -> dict:
    """
    Estimate budget for the event based on location and number of people.

    Args:
        number_of_people (int, optional): Number of attendees. Defaults to 1.
        location (str, optional): Location or venue for budget estimation. Defaults to "unknown".

    Returns:
        dict: Dictionary containing total and per person budget estimates with currency.
    """
    budget = estimate_budget(number_of_people, location)
    return {"budget_estimate": budget}
