from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional

class User(BaseModel):
    username: Annotated[str, Field(..., min_length=3)]
    email: EmailStr
    full_name: str
    role: Optional[str] = None
