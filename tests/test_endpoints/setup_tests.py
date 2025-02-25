
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from app.core.config import settings
from app.db.database import Base, get_async_session
from app.db.models import User, Task
from main import app   

async def get_test_session():
    try:
        engine = create_async_engine(settings.TEST_ASYNC_DATABASE_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)
        async with async_session_maker() as session:
            test_user = User(
                username = "username",
                email = "user@test.com",
                full_name = "full_name",
                password = "$2b$12$VnSYSL9LOr9GCn8FNwjuXOrIKRgTqFE2gKADg5t81ERziSUjuWbYK"
            )
            session.add(test_user)
            await session.commit()
            yield session
    finally: 
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()       
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        

app.dependency_overrides[get_async_session] = get_test_session

def client_decorator(func):
    async def wrapper():
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await func(client)
        return result
    return wrapper
    
