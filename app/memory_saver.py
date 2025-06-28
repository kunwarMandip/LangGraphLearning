import os
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt.chat_agent_executor import AgentState

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

checkpointer = InMemorySaver()

class WeatherResponse(BaseModel):
    conditions: str

def remember_name(name: str) -> str:
    """Remember the name of the user for future conversation"""
    return f"I'll remember the name of the user is  {name}"

def get_weather(location: str) -> str:
    """Get weather of a given location"""
    return f"Its always sunny in {location}!"

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config["configurable"].get("user_name")
    system_message = f"You are a helpful assistant. Address the user as: {user_name}"
    return [{"role": "system", "content": system_message}] + state["messages"]


agent = create_react_agent(
    model = ChatGroq(model = "llama-3.3-70b-versatile"),
    tools = [get_weather],
    prompt = prompt,
    checkpointer= checkpointer,
    response_format= WeatherResponse
)

config = {
    "configurable": {"thread_id": "1"},
    "recursion_limit": 20,
    "user_name": "John Smith",
}

sf_response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in sf?"}]}, 
    config
)

ny_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what about new york?"}]},
    config
)

ny_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what about new york?"}]},
)

print(sf_response)
print(ny_response)

sf_response["structured_response"]
ny_response["structured_response"]