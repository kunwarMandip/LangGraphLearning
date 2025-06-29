from typing import Annotated
from typing_extensions import TypedDict, List

from langgraph.graph.message import add_messages


# class Task1(TypedDict):

class MyState(TypedDict):
    messages:   Annotated[list, add_messages]

class SubDivideTask(TypedDict):
    easy_diff_tasks: List[str]
    medium_diff_tasks: List[str]
    hard_diff_tasks: List[str]
    

class EinsenhowerMatrix(TypedDict):
    urgent_important_tasks: List[str]
    non_urgent_important_tasks: List[str]
    delegable_tasks: List[str]
    ignorable_tasks: List[str]