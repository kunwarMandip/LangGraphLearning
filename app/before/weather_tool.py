import os
from dotenv import load_dotenv

import requests
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
llm = init_chat_model("openai:gpt-3.5-turbo")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
graph_builder = StateGraph(State)

def fetch_weather_data(location: str) -> str:
    """Fetches the weather data of a given location

    Args:
        location (str): the location of whose weather to find

    Returns:
        str: the temperature in the given location
    """
    url = f"http://api.weatherstack.com/current?access_key={weather_api_key}&query={location}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to retrieve weather data"
    
    data = response.json()
    
    weather_temp = data.get("current", {}).get("temperature", "N/A")
    return f"The temperature in {location} is {weather_temp} °C."


tools = [fetch_weather_data]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools)
graph_builder.add_edge(START, "chatbot")
 
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
            
            
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break