from datetime import datetime
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from pydantic_settings import BaseSettings

from app.db.database import Base


class Task(Base):
    __tablename__="task"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]
    text: Mapped[str]
    completd: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    time: Mapped[datetime]
    
class User(Base):
    __tablename__="user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str]
    full_name: Mapped[str]
    role: Mapped[str]
    
    