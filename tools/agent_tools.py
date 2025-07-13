# tools/agent_tools.py

from langchain.tools import tool
from agents.nlu_agent import parse_event_prompt
from agents.location_finder import find_places
from agents.event_scheduler import generate_feasible_slots
from agents.budget_estimator import estimate_budget

@tool
def nlu_tool(user_input: str) -> dict:
    """
    Parses the user's natural language input to extract event details.

    Args:
        user_input (str): The user's event planning query.

    Returns:
        dict: Extracted event details including event name, duration_hours,
              start_date, end_date, location, brand_name, query_type, and number_of_people.
    """
    return parse_event_prompt(user_input)


@tool
def location_finder_tool(location: str, query_type: str = "restaurant", brand_name: str = None) -> dict:
    """
    Finds nearby places based on provided location, query type, and brand name.

    Args:
        location (str): The region or locality to search within.
        query_type (str, optional): The type of place (e.g., restaurant, cafe). Defaults to "restaurant".
        brand_name (str, optional): Specific brand name to prioritize (e.g., McDonald's). Defaults to None.

    Returns:
        dict: Contains 'nearby_places', a list of matching place dictionaries with name, latitude, longitude, type, and category.
    """
    places = find_places(brand_name, query_type, location)
    return {"nearby_places": places}


@tool
def slot_generator_tool(start_date: str, end_date: str = None, duration_hours: int = 1) -> dict:
    """
    Generates feasible time slots for an event between start_date and end_date.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str, optional): End date in YYYY-MM-DD format. Defaults to start_date if None.
        duration_hours (int, optional): Duration of the event in hours. Defaults to 1.

    Returns:
        dict: Contains 'feasible_slots', a list of generated slot dictionaries with date, start_time, and end_time.
    """
    if end_date is None:
        end_date = start_date
    slots = generate_feasible_slots(start_date, end_date, duration_hours)
    return {"feasible_slots": slots}


@tool
def slot_selection_tool(event_name: str, feasible_slots: list) -> dict:
    """
    Selects the most suitable time slot based on the event type and context.

    Rules:
        - For 'date' events: prefer evening slots (17:00 onwards).
        - For 'lunch' events: prefer 12:00-15:00 slots.
        - For 'dinner' events: prefer slots after 19:00.
        - Defaults to the first available slot if no preference matches.

    Args:
        event_name (str): The name of the event to infer preferred time.
        feasible_slots (list): List of feasible slots generated earlier.

    Returns:
        dict: Contains 'selected_slot', the best matching slot dictionary.
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
    Estimates the budget for an event based on number of people and location.

    Args:
        number_of_people (int, optional): Number of guests attending. Defaults to 1.
        location (str, optional): Location of the event for cost reference. Defaults to "unknown".

    Returns:
        dict: Contains 'budget_estimate' with total budget and per person cost.
    """
    budget = estimate_budget(number_of_people, location)
    return {"budget_estimate": budget}
