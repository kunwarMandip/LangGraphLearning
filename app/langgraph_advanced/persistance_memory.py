#python -m app.langgraph_advanced.presistance_memory

import json
from langchain_core.tools import tool
from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate

from app.llm_info import llm

filename = "app\\langgraph_advanced\\data.json"

class State(TypedDict):
    latest_user_query: str
    # messages: Annotated[List, add_messages]


    
def create_prompt(user_input: str):
    chat_prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            """
                You are an information extraction assistant. Your task is to extract structured data from the user's input and return it in JSON format.

            Specifically, extract:
                * `name`: The person's full name, if mentioned. (string)
                * `age`: The person's age, if mentioned. (integer or null)
                * `description`: A list (array) of short descriptions about the person based on the input. Each time new relevant information appears, append a new string entry to this list. (array of strings)

            Respond with a **valid JSON object** only. No extra explanation or formatting.

            If a field is not provided in the input, set its value to `null` (for `name` and `age`) or an empty array (for `description`).

            Example output:
            {
                "name": "Alice Smith",
                "age": 28,
                "description": [
                    "A graphic designer who loves travel and coffee.",
                    "Currently based in Berlin."
                ]
            }
            
            The user data 
            """
        ),
        ("human", "{user_input}")
    ])
    
    return chat_prompt.format_messages(input=input)

def chatbot(state: State):
    user_query = state["latest_user_query"]
    messages = create_prompt(user_query)
    print(messages)
    return "extracting data"


def data_extraction(state: State):
    return "extracting data"

def normal_chat(state: State):
    return "normal chat"

@tool
def add_data(json_data):
    return "adding new data"

@tool
def get_user_data() -> str:
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
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


messages = {
    "latest_user_query": "Whats your name"
}

results = graph.invoke(messages)