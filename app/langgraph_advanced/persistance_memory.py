#python -m app.langgraph_advanced.persistance_memory

import json
from pydantic import BaseModel
from typing import Annotated, TypedDict, List

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.llm_info import llm

filename = "app\\langgraph_advanced\\data.json"

class State(TypedDict):
    latest_user_query: str
    messages: Annotated[List, add_messages]
    tool_called: bool  # Track if tool was called


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
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        
@tool
def save_user_data(user_data: UserData):
    """Save user data to file for future use"""
    print("Attempting to store user_data")
    
    # Load existing data
    existing_data = load_existing_data()
    
    # Update with new data (avoid duplicates)
    if user_data.user_name:
        print(f"Saving name: {user_data.user_name}")
        existing_data['user_name'] = user_data.user_name
    
    if user_data.order_details:
        print(f"Saving order details: {user_data.order_details}")
        if 'order_details' not in existing_data:
            existing_data['order_details'] = []
            
        # Only adding data if not already present
        for detail in user_data.order_details:
            if detail not in existing_data['order_details']:
                existing_data['order_details'].append(detail)
    
    if user_data.user_details:
        print(f"Saving user details: {user_data.user_details}")
        if 'user_details' not in existing_data:
            existing_data['user_details'] = []
        # Only add if not already present
        for detail in user_data.user_details:
            if detail not in existing_data['user_details']:
                existing_data['user_details'].append(detail)
    
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
            return json.dumps(data)
    except(FileNotFoundError):
        print("File not Found")
        return "{}"


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
            
            IMPORTANT RULES:
            1. DO NOT store any data that the user has not explicitly given for restaurant orders.
            2. Only save restaurant-related information (food orders, drinks, etc.)
            3. Do NOT save non-restaurant activities like sports, appointments, or general scheduling.
            4. If the user asks about non-restaurant activities, politely redirect them to restaurant services.
            5. Only call save_user_data when the user provides NEW restaurant order information.
            6. Do not repeatedly save the same information.
            
            Below is the data you currently have about the user:
            <User details:
                {user_details}
            >
            
            You should ONLY store these details about the user:
                - name (only if related to restaurant orders)
                - Restaurant Order Details (food, drinks, table reservations)
            """
        ),
        ("human", "{user_input}")
    ])
    
    return chat_prompt.format_messages(user_input=input, user_details=json.dumps(user_data))

def chatbot(state: State):
    print("On node: chatbot")
    user_query = state["messages"][-1].content
    print(f"Processing: {user_query}")
    
    # Skip processing if this is a tool response
    if isinstance(state["messages"][-1], AIMessage) and "Data saved successfully" in user_query:
        print("Skipping tool response message")
        return {"messages": []}
    
    prompt = create_prompt(user_query)
    print(f"Prompt created: {len(prompt)} messages")
    results = llm_with_tools.invoke(prompt)
    return {
        "messages": [results],
        "tool_called": bool(results.tool_calls) if hasattr(results, 'tool_calls') else False
    }

def should_continue(state: State):
    """Determine if we should continue to tools or end"""
    last_message = state["messages"][-1]
    
    # If the last message has tool calls, go to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    else:
        return "end"

def handle_tool_response(state: State):
    """Handle tool responses and prevent infinite loops"""
    print("Tool execution completed")
    return {"tool_called": False}

graph_builder = StateGraph(State)


graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Modified edges to prevent infinite loops
graph_builder.add_conditional_edges(
    "chatbot",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
graph_builder.add_edge("tools", END)
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

# Test with restaurant order
input_restaurant = {
    "messages": [
        {"role": "user", "content": "I'd like to order a pizza and a coke for table 5"}
    ]
}

print("=== Testing with restaurant order ===")
results = graph.invoke(input_restaurant)
print("Final result:", results)

print("\n" + "="*50 + "\n")

input_football = {
    "messages": [
        {"role": "user", "content": "Set me a time to play football for 2pm tomorrow"}
    ]
}

print("=== Testing with football request ===")
results = graph.invoke(input_football)
print("Final result:", results)



print("=== Testing with restaurant order ===")
results = graph.invoke(input_restaurant)
print("Final result:", results)

print("\n" + "="*50 + "\n")

# Test with non-restaurant request
name = {
    "messages": [
        {"role": "user", "content": "What is my name"}
    ]
}

print("=== Testing with football request ===")
results = graph.invoke(name)
print("Final result:", results)