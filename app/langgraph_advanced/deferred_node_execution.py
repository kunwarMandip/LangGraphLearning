#python -m app.langgraph_advanced.deferred_node_execution

from app.llm_info import llm
from langchain_core.tools import tool
from typing import Annotated, TypedDict
from langgraph.types import Command, interrupt
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

class State(TypedDict):
    messages: Annotated[list, add_messages]
    order_confirmed: bool = False

@tool
def human_confirmation(query: str) -> str:
    """Request confirmation from the customer."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tools = [human_confirmation]
llm_with_tools = llm.bind_tools(tools)

# def confirm_order(state: State):
#     """Node that waits for customer to confirm their order"""
#     messages = state["messages"]
    
#     confirmation_message = llm_with_tools.invoke([
#         {"role": "system", "content": "You are a restaurant order system. Ask the customer to confirm their order. Use the human_confirmation tool to get their response."},
#         {"role": "user", "content": f"Please confirm your order: {messages[-1]['content']}"}
#     ])
    
#     return {
#         "messages": [confirmation_message],
#         "order_confirmed": False
#     }

def confirm_order(state: State):
    """Node that waits for customer to confirm their order"""
    messages = state["messages"]
    
    # Access content of the last message using the correct attribute
    last_message_content = messages[-1].content if messages else "No previous messages"
    
    confirmation_message = llm_with_tools.invoke([
        {"role": "system", "content": "You are a restaurant order system. Ask the customer to confirm their order. Use the human_confirmation tool to get their response."},
        {"role": "user", "content": f"Please confirm your order: {last_message_content}"}
    ])
    
    return {
        "messages": [confirmation_message],
        "order_confirmed": False
    }

def prepare_food(state: State):
    """Node that prepares food only after order is confirmed"""
    messages = state["messages"]
    
    # Create a message about preparing the food
    preparation_message = llm_with_tools.invoke([
        {"role": "system", "content": "You are a restaurant kitchen system. The customer has confirmed their order. Now prepare the food and provide updates on the preparation process."},
        {"role": "user", "content": "The order has been confirmed. Please start preparing the food."}
    ])
    
    return {
        "messages": [preparation_message]
    }

def should_prepare_food(state: State):
    """Conditional logic to determine if food should be prepared"""
    # Check if we have a tool response indicating confirmation
    messages = state["messages"]
    if len(messages) > 0:
        last_message = messages[-1]
        # If the last message is from tools (confirmation received), proceed to prepare food
        if hasattr(last_message, 'name') and last_message.name == "human_confirmation":
            return "prepare_food"
    return END

# Build the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("confirm_order", confirm_order)
graph_builder.add_node("prepare_food", prepare_food)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Add edges
graph_builder.add_edge(START, "confirm_order")

# From confirm_order, go to tools (for human confirmation)
graph_builder.add_conditional_edges(
    "confirm_order",
    tools_condition
)

# From tools, decide whether to prepare food or end
graph_builder.add_conditional_edges(
    "tools",
    should_prepare_food
)

# After preparing food, end the process
graph_builder.add_edge("prepare_food", END)

# Compile the graph
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Example usage
if __name__ == "__main__":
    user_input = "I would like to order a pizza with pepperoni and mushrooms, and a cola."
    config = {"configurable": {"thread_id": "1"}}

    print("=== Restaurant Order System ===")
    print(f"Customer Order: {user_input}")
    print("\n" + "="*50 + "\n")

    # Start the graph
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()
    
    print("\n" + "="*50)
    print("Waiting for customer confirmation...")
    
    # Get human response
    human_response = input("Customer response: ")
    
    # Continue with the confirmation
    human_command = Command(resume={"data": human_response})
    
    print("\n" + "="*50 + "\n")
    
    events = graph.stream(human_command, config, stream_mode="values")
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()