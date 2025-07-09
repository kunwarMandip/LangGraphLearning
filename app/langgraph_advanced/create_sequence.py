
#python -m app.langgraph_advanced.create_sequence

import random
from typing import Annotated, TypedDict, List

from langgraph.pregel import RetryPolicy
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from app.llm_info import llm


class State(TypedDict):
    food: Annotated[List[AnyMessage], add_messages]
    
    
def take_order(state: State):
    print("take_order")
    return {
        "food": ["Taking Order"]
    }
    

def prepare_food(state: State):
    print("prepare_food")
    return {
        "food": ["Preparing Food"]
    }
def serve_food(state: State):
    print("serve_food")
    return {
        "food": ["Serving Food"]
    }
    
graph_builder = StateGraph(State)

graph_builder.add_node("take_order", take_order)
graph_builder.add_node("prepare_food", prepare_food)
graph_builder.add_node("serve_food", serve_food)

#START and END edges
graph_builder.add_edge(START, "take_order")
graph_builder.add_edge("take_order", "prepare_food")
graph_builder.add_edge("prepare_food", "serve_food")
graph_builder.add_edge("serve_food", END)

graph = graph_builder.compile()

results = graph.invoke({"food": []})

print(results["food"])
