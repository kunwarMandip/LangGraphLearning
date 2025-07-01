from app.task_1.llm_info import llm

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.task_1.states import MyState, SubDivideTask

def chatbot(state: MyState):
    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful assistant. Complete the user prompt step by step."
            "Identify the task given by the user. " +
            "Break down the task into sub parts so that i cant be tackled easily. "
        )
    }
    messages = [system_msg, *state["messages"]]
    reply = llm.invoke(messages)
    print(messages)
    print(reply.content)
    # print(reply)
    return {"messages": state["messages"] + [reply]}


def breakdown_tasks(state: MyState):    
    system_msg = {
        "role": "system",
        "content": (
            "You are an expert project manager. "
            "Break down the task given into Einsenhower matrix."
        )
    }
    messages = [system_msg, *state["messages"]]
    reply = llm.invoke(messages)
    print(messages)
    print(reply.content)
    return {"messages": state["messages"] + [reply]}


#Step 1 simple graph
def step_1():
    memory = MemorySaver()
    graph_builder = StateGraph(MyState)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("breakdown_tasks", breakdown_tasks)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", "breakdown_tasks")
    graph_builder.add_edge("breakdown_tasks", END)
    graph = graph_builder.compile(checkpointer=memory)
    return graph
