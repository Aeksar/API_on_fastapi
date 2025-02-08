from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id: int
    title: str
    text: str
    completd: bool = False
    time: datetime