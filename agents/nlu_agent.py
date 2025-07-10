from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from utils.date_utils import parse_relative_date
from dotenv import load_dotenv
import json
import re

load_dotenv()

llm = ChatGroq(model = 'compound-beta')

prompt_template = PromptTemplate(
    input_variables = ['current_date', 'user_input'],
    template = """
You are an event planner assistant. Today's date is {current_date}.

Extract from the user input:
- Event name
- Duration hours
- Start date (convert relative to absolute date in YYYY-MM-DD)
- End date (same as start unless otherwise specified)
- Location

Return in JSON format.

User input: {user_input}

"""
)

def parse_event_prompt(user_input):
    today = datetime.today().strftime('%Y-%m-%d')
    prompt = prompt_template.format(current_date = today, user_input = user_input)
    response = llm.invoke(prompt)
    return response

# if __name__ == "__main__":
#     user_prompt = "plan a casual lunch for 2 hours day after tomorrow around malad"
#     result = parse_event_prompt(user_prompt)

#     output_str = result  
#     output_text = output_str.content

#     json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
#     if json_match:
#         json_str = json_match.group()
#         parsed = json.loads(json_str)
#         print("----- NLU Agent Output -----")
#         print(parsed)
#     else:
#         print("No JSON found in output.")
