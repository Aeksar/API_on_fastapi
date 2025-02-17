import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient
from main import app

from app.db.database import get_async_session
from tests.test_endpoints.setup_testdb import get_test_session


app.dependency_overrides[get_async_session] = get_test_session


async def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "pupupupu"
    }
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/user/registration", json=user_data)

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["role"] == None
    assert created_user["password"] != user_data["password"]

async def test_show_all_user():  
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://tests"
    ) as client:
        response = await client.get("/user/1")
    body = response.json()
    assert body is not None
      
async def test_token():
    data = {
        "username": "username",
        "password": "password"
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://tests"
    ) as client:
        respose = await client.post(
            url="user/token", 
            data=data, 
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

    body = respose.json()
    headers = respose.headers
    cookie = respose.cookies
    
    assert respose.status_code == 200
    assert body["access_token"] is not None
    assert body["token_type"] == "Bearer"
    assert "Bearer" in  headers['authorization'] 
    assert cookie['access_token'] == body["access_token"] \
        and body["access_token"] in headers["authorization"]
    