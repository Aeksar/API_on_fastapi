from pydantic import BaseModel
from datetime import datetime

class TaskSchemas(BaseModel):
    id: int
    title: str
    text: str
    completed: bool = False
    time: datetime
    
class TaskCreate(BaseModel):
    title: str
    text: str
    
class TaskUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    completed: bool | None = None