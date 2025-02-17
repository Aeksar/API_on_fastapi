from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

from app.db.database import Base
from app.db.models import User
from app.api.schemas.user import UserFullSchema

async def find_by_id(session: AsyncSession, table: Type[Base], id):
    query = await session.execute(select(table).where(table.id == id))
    found = query.scalars().first()
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return found

def sqlalchemy_to_pydantic(user: User) -> UserFullSchema:
   return UserFullSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=user.password,
        role=user.role
    )