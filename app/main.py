import os
from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
llm = init_chat_model("openai:gpt-3.5-turbo")
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
                                                                 