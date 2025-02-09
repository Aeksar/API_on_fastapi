from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

from app.db.database import Base

async def find_by_id(session: AsyncSession, table: Type[Base], id):
    query = await session.execute(select(table).where(table.id == id))
    found = query.scalars().first()
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return found
