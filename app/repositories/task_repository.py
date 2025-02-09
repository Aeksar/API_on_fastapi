from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.api.schemas.task import TaskCreate, TaskUpdate
from app.db.models import Task, User


class TaskRepository(ABC):
    @abstractmethod
    async def get_tasks(self):
        pass
    
    @abstractmethod
    async def create_task(self, task: TaskCreate):
        pass
    
    @abstractmethod
    async def get_task(self, id):
        pass
    
    @abstractmethod
    async def update_task(self, id, modelUpdate: TaskUpdate):
        pass
    
    @abstractmethod
    async def delete_task(self, id):
        pass
    
    
class SQLAlchemyTaskRepository(TaskRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_tasks(self) -> list[Task]:
        query = await self.session.execute(select(Task))
        return query.scalars().all()
    
    async def create_task(self, task: TaskCreate, user_id: int):
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invailid user"
            )
        
        new_task = Task(**task.model_dump())
        new_task.time = datetime.now()
        new_task.creator = user
        
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        return new_task
        
    async def get_task(self, id):
        query = await self.session.execute(select(Task).where(Task.id == id))
        task = query.scalars().first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task now found"
            )
        return task
    
    async def update_task(self, id: int, modelUpdate: TaskUpdate) -> Task:
        query = await self.session.execute(select(Task).where(Task.id == id)) 
        task = query.scalars().first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task now found"
            )
        for key, value in modelUpdate.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def delete_task(self, id):
        query = await self.session.execute(select(Task).where(Task.id == id))
        task = query.scalars().first()
        if not task:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="don't found deleted user"
           )
        await self.session.delete(task)
        await self.session.commit()
        return True
        
        
        
        