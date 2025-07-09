
#python -m app.langgraph_advanced.presistance_memory
#python -m app.langgraph_advanced.persistance_memory

import json
from typing import Annotated, TypedDict, List
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from app.llm_info import llm

filename = "app\langgraph_advanced\data.json"

class State(TypedDict):
    food: Annotated[List[AnyMessage], add_messages]


def create_prompt():
    SYSTEM_PROMPT = {
        """
        You are an information extraction assistant. Your task is to extract structured data from the user’s input and return it in JSON format.

        Specifically, extract:
            * `name`: The person's full name, if mentioned. (string)
            * `age`: The person's age, if mentioned. (integer or null)
            * `description`: A list (array) of short descriptions about the person based on the input. Each time new relevant information appears, append a new string entry to this list. (array of strings)

        Respond with a **valid JSON object** only. No extra explanation or formatting.

        If a field is not provided in the input, set its value to `null` (for `name` and `age`) or an empty array (for `description`).

        Example output:

        ```json
        {
            "name": "Alice Smith",
            "age": 28,
            "description": [
                "A graphic designer who loves travel and coffee.",
                "Currently based in Berlin."
            ]
        }
    """
    }
    
def identify_query(state: State):
    return "extracting data"

def extract_json(state: State):
    return "extract json"

def save_to_json(data):
    # with open("data.json", "w") as f:
    #     json.dump(data, indent = 4)
    # return "saving"
    return "saving"

def read_json():
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            print(data)
            return data
    except(FileNotFoundError):
        print("File not Found")
        return {}
    return "reading"



graph_builder = StateGraph(State)

graph_builder.add_node("identify_query", identify_query)
graph_builder.add_node("extract_json", extract_json)
graph_builder.add_node("save_to_json", save_to_json)
graph_builder.add_node("read_json", read_json)

#START and END edges
graph_builder.add_edge(START, "identify_query")
graph_builder.add_edge("identify_query", "extract_json")
graph_builder.add_edge("extract_json", "save_to_json")
graph_builder.add_edge("save_to_json", END)

graph = graph_builder.compile()


data = read_json()
print(data)
