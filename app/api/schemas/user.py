from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated, Optional


class UserBaseSchema(BaseModel):
    username: Annotated[str, Field(..., min_length=3)]
    email: EmailStr
    full_name: str
    password:  Annotated[str, Field(min_length=8, )]
    
    # @field_validator("password")
    # def validate_pwd(cls, value: str):
    #     import re
    #     condition = r"^(?=.*[A-Z])(?=.[a-z])(?=.*[!@#$%^&*(),.])"
    #     if not re.match(condition, value):
    #         raise ValueError(
    #             "Пароль должен содержать минимум 8 символов,"
    #             "1 заглавную, 1 строчную буквы и спец. символ"
    #         )
    
class UserFullSchema(BaseModel):
    id: int
    username: Annotated[str, Field(..., min_length=3)]
    email: EmailStr
    full_name: str
    password:  Annotated[str, Field(min_length=8, )]
    role: Optional[str] = None
    
class UserUpdate(UserBaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    
