import os
from langchain.chat_models import init_chat_model

os.environ["LLAMA_API_KEY"] = "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"

llm = init_chat_model("llama-3.3-70b-versatile")

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


def chatbot(state: State):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
                                                                 