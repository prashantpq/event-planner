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
    budget_estimator_tool
)

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=GROQ_API_KEY)

TOOLS = {
    "nlu_tool": nlu_tool,
    "slot_generator_tool": slot_generator_tool,
    "location_finder_tool": location_finder_tool,
    "budget_estimator_tool": budget_estimator_tool,
}

def extract_json(text):
    json_pattern = re.compile(r"\{(?:[^{}]|(?R))*\}", re.DOTALL)
    match = json_pattern.search(text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Raw matched string:", match.group())
            return None
    return None


messages = [
    {
        "role": "system",
        "content": (
            "You are an event planning agent.\n"
            "Always output a single valid JSON object with double quotes and no extra text, explanation, or markdown.\n"
            "Available tools: nlu_tool, slot_generator_tool, location_finder_tool, budget_estimator_tool.\n"
            "Example: {\"tool\": \"nlu_tool\", \"args\": {\"user_input\": \"Plan dinner tomorrow in Malad\"}}.\n"
            "If the plan is complete, respond with:\n"
            "{\"tool\": \"finish\", \"args\": {\"result\": \"<final_plan_here>\"}}."
        )
    }
]

print("----- Running Groq Agentic Event Planner (Full Loop) -----")
user_input = input("Enter your event planning request: ")
messages.append({"role": "user", "content": user_input})

while True:
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",  
            messages=messages,
            temperature=0.3
        )

        content = response.choices[0].message.content
        print("🔎 LLM OUTPUT:", content)

        parsed = extract_json(content)
        if not parsed:
            print("No valid JSON parsed. Ending.")
            break

        tool_name = parsed.get("tool")
        args = parsed.get("args", {})

        if tool_name == "finish":
            print("FINAL PLAN:", args.get("result"))
            break

        tool_func = TOOLS.get(tool_name)
        if tool_func:
            print(f"🔧 Calling tool: {tool_name} with args: {args}")
            result = tool_func.invoke(args)
            print(f"{tool_name} result:", result)
            messages.append({"role": "assistant", "content": json.dumps(parsed)})
            messages.append({"role": "user", "content": json.dumps(result)})

        else:
            print(f"Unknown tool: {tool_name}. Ending.")
            break

    except RateLimitError as e:
        retry_after = getattr(e, 'retry_after', 2)
        print(f"⏳ Rate limit hit. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)

    except KeyboardInterrupt:
        print("\n Interrupted by user.")
        break

    except Exception as e:
        print("Unexpected error:", e)
        break
