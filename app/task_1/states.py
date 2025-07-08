from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal
from typing_extensions import TypedDict, List

from langgraph.graph.message import add_messages

class EisenhowerMatrix(Enum):
    URGENT_IMPORTANT: 1
    URGENT_NOT_IMPORTANT: 2
    IMPORTANT_NOT_URGENT: 3
    IGNORABLE: 4
    
class SubTask(BaseModel):
    description: str
    priority: int
    completed: bool = False
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

class TaskState(BaseModel):
    goal: str
    priority: int
    subtasks: List[SubTask] = []
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
class MyState(TypedDict):
    messages: Annotated[list, add_messages]
  
    