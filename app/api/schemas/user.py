from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional


class UserCreate(BaseModel):
    username: Annotated[str, Field(..., min_length=3)]
    email: EmailStr
    full_name: str
    
class UserSchema(UserCreate):
    id: int
    role: Optional[str] = None
    
class UserUpdate(UserCreate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None