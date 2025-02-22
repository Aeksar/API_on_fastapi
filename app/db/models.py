from datetime import datetime
from sqlalchemy import DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic_settings import BaseSettings
from typing import List

from app.db.database import Base

class Task(Base):
    __tablename__="task"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]
    text: Mapped[str]
    completd: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    time: Mapped[datetime]
    
    creator: Mapped["User"] = relationship(back_populates="tasks")
    
    
class User(Base):
    __tablename__="user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str]
    full_name: Mapped[str]
    role: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    
    tasks: Mapped[List["Task"]] = relationship(back_populates="creator")
   
    
class Comment(Base):
    __tablename__="comment"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner: Mapped[int] = mapped_column(ForeignKey("user.id"))
    f_task: Mapped[int] = mapped_column(Integer, ForeignKey('task.id'))
    text: Mapped[str]
    date: Mapped[datetime]