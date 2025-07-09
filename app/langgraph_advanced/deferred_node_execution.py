#python -m app.langgraph_advanced.deferred_node_execution

# In the restaurant order system, sometimes a customer may choose to delay their order.
# Create a graph where a node for the "prepare food" step is deferred until triggered by a "confirm order" node.
# Instructions:
# Create a graph with 2 nodes:
# Confirm order (wait for the customer to confirm the order).
# Prepare food (only starts when the customer confirms).
# Ensure that the "Prepare food" node does not execute until the "Confirm order" node is triggered.
# Display a message confirming the customer’s order and then proceed to prepare the food.

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

@tool
def human_confirmation(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tools = [human_confirmation]
llm_with_tools = llm.bind_tools(tools)

def prepare_food(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {
        "messages": [message]
    }


graph_builder = StateGraph(State)

graph_builder.add_node("prepare_food", prepare_food)
tool_node = ToolNode(tools = tools)
graph_builder.add_node("tools", tool_node)

#START and END nodes
graph_builder.add_conditional_edges(
    "prepare_food", 
    tools_condition
)
graph_builder.add_edge("tools", "prepare_food")
graph_builder.add_edge(START, "prepare_food")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer = memory)

user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
        
        
human_response = input("Should you continue?")


human_command = Command(resume={"data": human_response})

events = graph.stream(human_command, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()