import json
import time
import os
import regex as re
from groq import Groq
from dotenv import load_dotenv
from groq._exceptions import RateLimitError

from tools.agent_tools import (
    nlu_tool,
    slot_generator_tool,
    location_finder_tool,
    budget_estimator_tool,
    slot_selection_tool
)

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=GROQ_API_KEY)

TOOLS = {
    "nlu_tool": nlu_tool,
    "slot_generator_tool": slot_generator_tool,
    "location_finder_tool": location_finder_tool,
    "budget_estimator_tool": budget_estimator_tool,
    "slot_selection_tool": slot_selection_tool,
}

def extract_json(text):
    """
    Extract JSON content from text using regex.
    """
    json_pattern = re.compile(r"\{(?:[^{}]|(?R))*\}", re.DOTALL)
    match = json_pattern.search(text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None

def build_final_output(event_name, slot, place, number_of_people, budget_estimate):
    """
    Build the final structured event plan output.
    """
    return f"""
Here's your recommended event plan!

Event: {event_name.title()}
Date: {slot['date']}
Time: {slot['start_time']} to {slot['end_time']}
Location: {place['name']}
Guests: {number_of_people}
Total Budget: {budget_estimate['currency']}{budget_estimate['total_budget']}
Per Person: {budget_estimate['currency']}{budget_estimate['per_person_cost']}

Enjoy your {event_name.lower()}!
""".strip()

# System prompt setup
messages = [
    {
        "role": "system",
        "content": (
            "You are EventPlanner, a friendly and professional event planning assistant.\n"
            "If user input is chit-chat or general questions, respond conversationally.\n"
            "If user requests event planning, output a single valid JSON with tool calls.\n"
            "Available tools: nlu_tool, slot_generator_tool, slot_selection_tool, location_finder_tool, budget_estimator_tool.\n"
            "When providing feasible slots or nearby places, output them as lists before finalizing the plan.\n"
            "When calling location_finder_tool, ensure you pass both location and query_type.\n"
            "Use slot_generator_tool after parsing event details and pass start_date, end_date, and duration_hours.\n"
            "Use slot_selection_tool after generating feasible slots to select the best slot based on event type and user context.\n"
            "When calling slot_selection_tool, ensure you pass both event_name and feasible_slots.\n"
            "Example: {\"tool\": \"nlu_tool\", \"args\": {\"user_input\": \"Plan dinner tomorrow in Malad\"}}.\n"
            "When the plan is ready, respond with:\n"
            "{\"tool\": \"finish\", \"args\": {\"result\": \"<final_plan_here>\"}}."
        )
    }
]

print("----- Welcome to Event Planner AI -----")
user_input = input("You: ")
messages.append({"role": "user", "content": user_input})

event_data = {}

while True:
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.3
        )

        content = response.choices[0].message.content
        parsed = extract_json(content)

        if parsed and parsed.get("tool"):
            tool_name = parsed["tool"]
            args = parsed.get("args", {})

            if tool_name == "finish":
                print("\n Final Event Plan:")
                print(args.get("result"))
                break

            tool_func = TOOLS.get(tool_name)
            if tool_func:
                print(f"\n🔧 Executing {tool_name}...")
                result = tool_func.invoke(args)
                messages.append({"role": "assistant", "content": json.dumps(parsed)})
                messages.append({"role": "user", "content": json.dumps(result)})

                # Display venues if returned
                if tool_name == "location_finder_tool":
                    venues = result.get("nearby_places")
                    if venues:
                        print("\n ---------- AVAILABLE VENUES ----------")
                        for idx, place in enumerate(venues, 1):
                            print(f"{idx}. {place['name']} (Lat: {place['latitude']}, Lon: {place['longitude']})")
                    else:
                        print("\nNo venues found for the specified query and location.")

                # Display slots if returned
                if tool_name == "slot_generator_tool":
                    slots = result.get("feasible_slots")
                    if slots:
                        print("\n ---------- AVAILABLE SLOTS ----------")
                        for idx, slot in enumerate(slots, 1):
                            print(f"{idx}. Date: {slot['date']}, Time: {slot['start_time']} to {slot['end_time']}")
                    else:
                        print("\nNo feasible slots found.")

                event_data.update(result)

            else:
                print(f"⚠️ Unknown tool: {tool_name}")
                break

        else:
            print('\n')
            print(f"AI: {content}")
            print('\n')
            user_input = input("You: ")
            messages.append({"role": "user", "content": user_input})

    except RateLimitError as e:
        retry_after = getattr(e, 'retry_after', 2)
        print(f" Rate limit hit. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)

    except KeyboardInterrupt:
        print("\n Exiting. Goodbye!")
        break

    except Exception as e:
        print("⚠️ Unexpected error:", e)
        break

# Final structured plan output
try:
    if all(k in event_data for k in ["feasible_slots", "nearby_places", "budget_estimate"]):
        selected_slot = event_data.get("selected_slot") or event_data["feasible_slots"][0]
        venues = event_data.get("nearby_places", [])
        selected_place = venues[0] if venues else {"name": "No venue found", "latitude": "", "longitude": ""}

        number_of_people = event_data.get("number_of_people", "N/A")
        budget_estimate = event_data["budget_estimate"]
        event_name = event_data.get("event_name", "Event")

        final_plan = build_final_output(
            event_name=event_name,
            slot=selected_slot,
            place=selected_place,
            number_of_people=number_of_people,
            budget_estimate=budget_estimate
        )
        print("\n ---------- FINAL STRUCTURED PLAN ----------")
        print(final_plan)
    else:
        print("\n⚠️ Could not build final structured plan due to missing data.")
except Exception as e:
    print("⚠️ Error building final structured plan:", e)
