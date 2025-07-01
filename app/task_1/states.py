from enum import enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal
from typing_extensions import TypedDict, List

from langgraph.graph.message import add_messages

class MyState(TypedDict):
    messages:   Annotated[list, add_messages]

class EisenhowerMatrix(enum):
    URGENT_IMPORTANT: 1
    URGENT_NOT_IMPORTANT: 2
    IMPORTANT_NOT_URGENT: 3
    IGNORABLE: 4
    
class SubTask(BaseModel):
    description: str
    priority: EisenhowerMatrix
    completed: bool = False
    deadline = Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    deadline: datetime = Field(default_factory=datetime.now)

class TaskState(BaseModel):
    goal: str
    priority: EisenhowerMatrix
    subtasks: List[SubTask] = []
    created_at: datetime = Field(default_factory=datetime.now)
    deadline: datetime = Field(default_factory=datetime.now)