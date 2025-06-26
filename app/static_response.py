from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain.schema import AIMessage  

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def static_chatbot(state: State):
    """No need for state here"""
    return {"messages": [AIMessage(content="static message")]}
    

graph_builder.add_node("static", static_chatbot)
graph_builder.add_edge(START, "static")
graph = graph_builder.compile()
graph.invoke({})


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input)