import asyncio, pytest, pytest_asyncio, httpx
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession
)
from app.core.config import settings
from app.db.database import Base, get_async_session
from main import app


TEST_DATABASE_URL = settings.TEST_ASYNC_DATABASE_URL

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(url=TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all(bind=engine))
        
    yield engine
    
    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all())
    await engine.dispose()
    
@pytest_asyncio.fixture(scope="session")
async def test_session(test_engine: AsyncEngine):

    test_sessionmaker = async_sessionmaker(bind=test_engine, class_=AsyncSession)
    async with test_sessionmaker() as session:
        yield session
    
@pytest_asyncio.fixture()
async def override_dependencies(test_session: AsyncSession):
    async def get_test_async_session():
        yield test_session
    
    app.dependency_overrides[get_async_session] = get_test_async_session 
    yield
    app.dependency_overrides.clear()
    
@pytest_asyncio.fixture()
def test_client(override_dependencies):
    with TestClient(app) as client:
        return client
