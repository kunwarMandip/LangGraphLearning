#python -m app.langgraph_advanced.persistance_memory

import json
from pydantic import BaseModel
from langchain_core.tools import tool
from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode, tools_condition


from app.llm_info import llm

filename = "app\\langgraph_advanced\\data.json"

class State(TypedDict):
    latest_user_query: str
    messages: Annotated[List, add_messages]


class UserData(BaseModel):
    user_name: str = None
    order_details: List[str] = None 
    user_details: List[str] = None
            
@tool
def save_user_data(user_data: UserData):
    """Save user data to file for future use"""
    print("Attempting to store user_data")
    
    if user_data.user_name:
        print("save name")
    
    if user_data.order_details:
        print("saving userData")

    if user_data.user_details:
        print(user_data.user_details)
        
    return "data saved"
    
@tool
def get_user_data() -> str:
    """Get the data about user and user orders"""
    print("Attempting to get user_data")
    
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            print(data)
            return data
    except(FileNotFoundError):
        print("File not Found")
        return {}


tools = [save_user_data, get_user_data]
llm_with_tools = llm.bind_tools(tools)

def create_prompt(user_input: str):
    chat_prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            """
                You are an friendly restaurant diner assistant.
                Your task is to collect user data and store them for future use.
            """
        ),
        ("human", "{user_input}")
    ])
    
    return chat_prompt.format_messages(user_input=user_input)

def chatbot(state: State):
    print("On node: chatbot")
    user_query = state["messages"][-1].content
    print(user_query)
    prompt = create_prompt(user_query)
    print(prompt)
    results = llm_with_tools.invoke(prompt)
    return {
        "messages": results
    }


graph_builder = StateGraph(State)

#Specifying Nodes
graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools= tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


input_2 = {
    "messages": [
        {"role": "user", "content": "Set me a time to play football for 2pm tomorrow"}
    ]
}

results = graph.invoke(input_2)
print(results)