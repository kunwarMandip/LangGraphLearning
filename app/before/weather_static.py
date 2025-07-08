# app/weather_checker.py
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Step 1: Define state
class WeatherState(TypedDict):
    messages: Annotated[list, add_messages]
    location: str
    weather: str

# Step 2: Mock weather data
weather_data = {
    "london": "Rainy, 17°C",
    "new york": "Sunny, 25°C",
    "paris": "Cloudy, 20°C",
}

# Step 3: Node - extract location
def get_location(state: WeatherState) -> WeatherState:
    last_user_message = state["messages"][-1]["content"]
    location = last_user_message.strip().lower()
    return {**state, "location": location}

# Step 4: Node - check weather
def check_weather(state: WeatherState) -> WeatherState:
    location = state["location"]
    weather = weather_data.get(location, "Location not found")
    return {**state, "weather": weather}

# Step 5: Node - format final response
def format_response(state: WeatherState) -> str:
    location = state["location"].title()
    weather = state["weather"]
    return f"Weather in {location}: {weather}"

# Step 6: Build the LangGraph
graph_builder = StateGraph(WeatherState)
graph_builder.add_node("get_location", get_location)
graph_builder.add_node("check_weather", check_weather)
graph_builder.add_node("format_response", format_response)

graph_builder.set_entry_point("get_location")
graph_builder.add_edge("get_location", "check_weather")
graph_builder.add_edge("check_weather", "format_response")
graph_builder.set_finish_point("format_response")

graph = graph_builder.compile()


if __name__ == "__main__":
    # from langgraph.graph import message

    user_input = input("Enter your location: ")
    initial_state = {
        "messages": [{"role": "user", "content": user_input}],
        "location": "",
        "weather": ""
    }

    output = graph.invoke(initial_state)
    print(output)