import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def get_weather(location: str) -> str:
    """Get weather of a given location"""
    return f"Its always sunny in {location}!"

agent = create_react_agent(
    model = ChatGroq(model = "llama-3.3-70b-versatile"),
    tools = [get_weather],
    prompt = "You are a helpful assistant"
)

results = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in london?"}]}
)

print (results)

