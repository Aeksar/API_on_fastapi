from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

class CommSchemas(BaseModel):
    comm_id: int
    user_id: int
    task_id: int
    text: str
    date: datetime
    
class CommCreate(BaseModel):
    text: Annotated[str, Field(max_length=150)]

class CommUpdate(BaseModel):
    comm_id: int
    text: str | None = None
    
