import os
from dotenv import load_dotenv


from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

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
    prompt = prompt
)

results =  agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config={
        "configurable": {"user_name": "John Smith"},
        "recursion_limit": 20
    },
)

print (results)