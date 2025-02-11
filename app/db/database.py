from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
import asyncio

engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)



class Base(DeclarativeBase):
    pass


async def get_async_session():
    try:
        async with async_session_maker() as session:
            yield session
    except Exception as e:
        print(f"Ошибка подключения к бд {e}")
        raise
        

# async def create_drop_db():
#     engine = create_async_engine(url=settings.ASYNC_DATABASE_URL)

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# asyncio.run(create_drop_db())