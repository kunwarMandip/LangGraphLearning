import random
from typing import Annotated, TypedDict, List

from langgraph.pregel import RetryPolicy
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from app.llm_info import llm

#python -m app.langgraph_advanced.task_1.graph

class State(TypedDict):
    logs: List[str]
    order: str


def process_food(state: State):
    
    logs = state.get("logs", [])
    
    if random.random() < 0.7:
        print("failing")
        raise Exception("Simulated Failure")

    logs.append("Food processed")
    state["logs"] = logs

    return {
        "logs": logs, 
        "state": "pizza"
    }


graph_builder = StateGraph(State)
graph_builder.add_node("process_food", process_food, retry_policy=RetryPolicy())
graph_builder.add_edge(START, "process_food")
graph_builder.add_edge("process_food", END)
graph = graph_builder.compile()

print("Graph created successfully")
print(graph)


initial_state = {"logs": [], "order": ""}

try:
    results = graph.invoke(initial_state)
    print("Order:", results["order"])
    print("Logs:", results["logs"])
except Exception as e:
    print(f"Error occurred: {e}")
    print("This might be due to the simulated failures or missing dependencies")