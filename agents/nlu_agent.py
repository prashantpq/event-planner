# agents/nlu_agent.py

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from dotenv import load_dotenv
import json
import re

load_dotenv()

llm = ChatGroq(model='compound-beta')

prompt_template = PromptTemplate(
    input_variables=['current_date', 'user_input'],
    template="""
You are an event planner assistant. Today's date is {current_date}.

Extract from the user input:
- Event name
- Duration hours
- Start date (convert relative to absolute date in YYYY-MM-DD)
- End date (same as start unless otherwise specified)
- Location
- Number of people (if not mentioned, assume 2)
- Query type (bar, cafe, restaurant, pub, club, McDonald's, Starbucks etc. Infer from user input. Default to "restaurant" if not clear.)

Return only valid JSON without any explanation or text before or after it.

User input: {user_input}
"""
)



def parse_event_prompt(user_input):
    today = datetime.today().strftime('%Y-%m-%d')
    prompt = prompt_template.format(current_date=today, user_input=user_input)
    response = llm.invoke(prompt)

    output_str = response.content if hasattr(response, 'content') else str(response)

    # Debug print raw output
    print("DEBUG LLM OUTPUT:\n", output_str)

    # Extract first JSON object block (simple approach)
    json_match = re.search(r'\{.*?\}', output_str, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        try:
            parsed = json.loads(json_str)
            return parsed
        except Exception as e:
            return {"error": f"JSON parsing failed: {e}\nRaw JSON string: {json_str}"}
    else:
        return {"error": "No JSON found in model response.\nFull output: " + output_str}




if __name__ == "__main__":
    user_input = "plan a dinner tomorrow for 3 hours for 4 people in malad"
    result = parse_event_prompt(user_input)
    print(result)
