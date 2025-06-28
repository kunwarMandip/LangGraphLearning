
from dataclasses import dataclass, field
from typing import Optional
 
@dataclass
class ChatState:
    user_name: Optional[str] = None
    
