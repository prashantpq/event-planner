import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="compound-beta")

prompt_template = PromptTemplate(
    input_variables=["current_date", "user_input"],
    template="""
You are an event planner assistant. Today's date is {current_date}.

Extract from the user input:
- Event name
- Duration hours
- Start date (convert relative to absolute date in YYYY-MM-DD)
- End date (same as start unless otherwise specified)
- Location

Return **only valid JSON** with double quotes, no explanation.

User input: {user_input}
"""
)

def parse_event_prompt(user_input):
    today = datetime.today().strftime('%Y-%m-%d')
    prompt = prompt_template.format(current_date=today, user_input=user_input)
    response = llm.invoke(prompt)

    output_str = response.content if hasattr(response, 'content') else str(response)

    # Extract only JSON block using regex
    json_match = re.search(r'\{.*\}', output_str, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        try:
            parsed = json.loads(json_str)
            return parsed
        except json.JSONDecodeError as e:
            print("JSON parsing error:", e)
            print("Received string:", json_str)
            return {"error": "Invalid JSON format from NLU agent"}
    else:
        print("No JSON found in output.")
        print("Full output:", output_str)
        return {"error": "No JSON found in NLU output"}
