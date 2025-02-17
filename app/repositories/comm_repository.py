from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.api.schemas.comment import CommCreate, CommUpdate, CommSchemas
from app.db.models import Task, User, Comment


class CommRepository(ABC):
    
    @abstractmethod
    async def create_comm(self, comm: CommCreate, username: str, task_id: int):
        pass
    
    @abstractmethod
    async def update_comm(self, id, modelUpdate: CommUpdate):
        pass
    
    @abstractmethod
    async def user_comms(self, user_id: int) -> list[CommSchemas]:
        pass
    
    @abstractmethod
    async def delete_comm(self, id):
        pass
    
    @abstractmethod
    async def task_comms(self, id):
        pass
    
    
class SQLAlchemyCommRepository(CommRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_comm(self, comm: CommCreate, username: str, task_id: int) -> Comment:
        user_query = await self.session.execute(select(User).where(User.username == username))
        user = user_query.scalars().first()
        task = await self.session.get(Task, task_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invailid user"
            )
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        new_comm = Comment(**comm.model_dump())
        new_comm.date = datetime.now()
        new_comm.owner = user.id
        new_comm.f_task = task.id
        
        self.session.add(new_comm)
        await self.session.commit()
        await self.session.refresh(new_comm)
        return new_comm
    

    async def user_comms(self, user_id) -> list[CommSchemas]:
        query = await self.session.execute(select(Comment).where(Comment.owner == user_id))
        return query.scalars().all()
   
    async def task_comms(self, task_id) -> list[CommSchemas]:
        query = await self.session.execute(select(Comment).where(Comment.f_task == task_id))
        return query.scalars().all()
   
    async def update_comm(self, id: int, modelUpdate: CommUpdate) -> Comment:
        query = await self.session.execute(select(Comment).where(Comment.id == id)) 
        task = query.scalars().first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment now found"
            )
        for key, value in modelUpdate.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def delete_comm(self, id) -> bool:
        query = await self.session.execute(select(Comment).where(Comment.id == id))
        task = query.scalars().first()
        if not task:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="don't found deleted comments"
           )
        await self.session.delete(task)
        await self.session.commit()
        return True
        