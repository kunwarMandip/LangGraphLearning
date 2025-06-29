from app.task_1.llm_info import llm

from langgraph.graph import StateGraph, START, END
from app.task_1.states import MyState, SubDivideTask

def chatbot(state: MyState):
    return {"messages": [llm.invoke(state["messages"])]}

#Step 1 simple graph
def step_1():
    graph_builder = StateGraph(MyState)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, chatbot)
    graph_builder.add_edge(chatbot, END)
    graph = graph_builder.compile()
    return graph