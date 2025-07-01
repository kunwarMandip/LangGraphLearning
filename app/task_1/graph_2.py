from app.task_1.llm_info import llm

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def identify_query(state):
    return "starting chatbot"

def add_task(state):
    return "adding a new task"

def identify_sub_task():
    return "create a list of sub tasks dependant on task"

def add_sub_tasks():
    return "creating sub_tasks"

def update_task(state):
    return "updating a current task"

def update_sub_task(state):
    return "updating a task sub task"

def verify_tasks():
    return "verifying tasks"


memory = MemorySaver()
graph_builder = StateGraph()

#Create nodes
graph_builder.add_node("identify_query", identify_query)
graph_builder.add_node("add_tasks", add_task)
graph_builder.add_node("identify_sub_tasks", identify_sub_task)
graph_builder.add_node("add_sub_tasks", add_sub_tasks)
graph_builder.add_node("update_tasks", update_task)
graph_builder.add_node("update_sub_task", update_sub_task)
graph_builder.add_node("verify_tasks", verify_tasks)

#Set START and END edge
graph_builder.add_edge(START, "identify_query")
graph_builder.add_edge("verify_tasks", END)

#Create conditional edges

graph_builder.a(identify_query, )
graph_builder.add_edge()
graph_builder.add_edge()
graph_builder.add_edge()
graph_builder.add_edge()


graph_builder.add

graph = graph_builder.compile(checkpointer=memory)
