import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()

os.environ('GROQ_API_KEY')


search_tool = DuckDuckGoSearchRun()

result = search_tool.invoke('top news today')
print(result)

llm = ChatGroq(model = 'distil-whisper-large-v3-en')
