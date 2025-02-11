from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.api.schemas.user import UserBaseSchema, UserFullSchema, UserUpdate
from app.db.models import Task, User
from app.repositories.rep_utils import find_by_id

class UserRepository(ABC):
    @abstractmethod
    async def get_users(self):
        pass
    
    @abstractmethod
    async def create_user(self, userC: UserBaseSchema):
        pass
    
    @abstractmethod
    async def get_user(self, id: int):
        pass
    
    @abstractmethod
    async def update_user(self, id: int, userU: UserUpdate):
        pass
    
    @abstractmethod
    async def delete_user(self, id: int):
        pass
    
    @abstractmethod
    async def user_task(self, id: int):
        pass
    

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_users(self):
        query = await self.session.execute(select(User))
        return query.scalars().all()
      
    async def create_user(self, userC: UserBaseSchema):
        new_user = User(**userC.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def get_user(self, user_id: int):
        user = await find_by_id(self.session, User, user_id)
        return user
    
    async def update_user(self, user_id: int, userU: UserUpdate):
        user = await find_by_id(self.session, User, user_id)
        for key, val in userU.model_dump(exclude_unset=True).items():
            setattr(user, key, val)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete_user(self, user_id: int):
        user = await find_by_id(self.session, User, user_id)
        await self.session.delete(user)
        await self.session.commit()
        return True
    
    async def user_task(self, user_id):
        query = await self.session.execute(select(Task).where(Task.created_by == user_id))
        return query.scalars().all()

        
        
        
        