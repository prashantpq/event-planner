# main.py

from agents.nlu_agent import parse_event_prompt
from agents.event_scheduler import generate_feasible_slots
from agents.location_finder import find_places
from agents.budget_estimator import estimate_budget

def orchestrate(user_input):
    parsed = parse_event_prompt(user_input)
    if "error" in parsed:
        return {"status": "fail", "message": parsed["error"]}

    event_name = parsed.get("event_name")
    duration_hours = parsed.get("duration_hours")
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")
    location = parsed.get("location")
    num_people = parsed.get("num_people", 2)

    slots = generate_feasible_slots(start_date, end_date, duration_hours)
    places = find_places(query="restaurant", region=location)
    budget = estimate_budget(duration_hours, num_people, location)

    return {
        "status": "success",
        "event_name": event_name,
        "date_range": [start_date, end_date],
        "duration_hours": duration_hours,
        "num_people": num_people,
        "feasible_slots": slots,
        "nearby_places": places,
        "budget_estimate": budget
    }


if __name__ == "__main__":
    user_prompt = "plan a casual lunch for 2 hours day after tomorrow around malad for 3 people"
    result = orchestrate(user_prompt)

    print("----- Final Planner Output -----\n")

    if result['status'] == 'success':
        print(f"✅ Event: {result['event_name'].title()}")
        print(f"📅 Date Range: {result['date_range'][0]} to {result['date_range'][1]}")
        print(f"⏳ Duration: {result['duration_hours']} hours")
        print(f"👥 Number of people: {result.get('num_people', 2)}\n")

        print("🕒 Feasible Slots:")
        for slot in result['feasible_slots']:
            print(f" - {slot['start_time']} to {slot['end_time']} on {slot['date']}")

        print("\n🍽 Nearby Restaurants:")
        if result['nearby_places']:
            for place in result['nearby_places']:
                print(f" - {place['name']} (Lat: {place['latitude']}, Lon: {place['longitude']})")
        else:
            print("No nearby restaurants found.")

        print(f"\n💰 Estimated Budget: {result['budget_estimate']['total_budget']} {result['budget_estimate']['currency']} "
              f"({result['budget_estimate']['per_person_cost']} per person)")

    else:
        print(f"❌ Failed: {result['message']}")
