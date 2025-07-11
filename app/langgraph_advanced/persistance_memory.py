#python -m app.langgraph_advanced.persistance_memory

import json
from pydantic import BaseModel
from typing import Annotated, TypedDict, List

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
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
            

def load_existing_data():
    """Helper function to load existing data from file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_data_to_file(data):
    """Helper function to save data to file"""
    # Ensure directory exists
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        
@tool
def save_user_data(user_data: UserData):
    """Save user data to file for future use"""
    print("Attempting to store user_data")
    
    # Load existing data
    existing_data = load_existing_data()
    
    # Update with new data
    if user_data.user_name:
        print(f"Saving name: {user_data.user_name}")
        existing_data['user_name'] = user_data.user_name
    
    if user_data.order_details:
        print(f"Saving order details: {user_data.order_details}")
        if 'order_details' not in existing_data:
            existing_data['order_details'] = []
        existing_data['order_details'].extend(user_data.order_details)
    
    if user_data.user_details:
        print(f"Saving user details: {user_data.user_details}")
        if 'user_details' not in existing_data:
            existing_data['user_details'] = []
        existing_data['user_details'].extend(user_data.user_details)
    
    # Actually save to file
    save_data_to_file(existing_data)
    return "Data saved successfully"

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

def create_prompt(input: str):
    # Get user data directly here instead of calling tool in prompt
    user_data = load_existing_data()
    
    chat_prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            """
            You are a friendly restaurant diner assistant.
            Your task is to take user order details and answer any questions the user may have about their orders.
            DO NOT store any data that the user has not explicitly given.
            
            Below is the data you currently have about the user:
            <User details:
                {user_details}
            >
            
            You should ONLY store these details about the user:
                - name 
                - Order Details
                
            Important: Only call save_user_data when the user provides new information that needs to be stored.
            Do not repeatedly try to save the same information.
            """
        ),
        ("human", "{user_input}")
    ])
    
    return chat_prompt.format_messages(user_input=input, user_details=json.dumps(user_data))

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