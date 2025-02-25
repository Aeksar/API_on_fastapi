import pytest
from httpx import AsyncClient

from tests.test_endpoints.setup_tests import get_test_session, client_decorator


@client_decorator
async def test_create_user(client: AsyncClient):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "pupupupu"
    }
    
    response = await client.post("/user/registration", json=user_data)

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["role"] == None
    assert created_user["password"] != user_data["password"]


@client_decorator
async def test_show_all_user(client: AsyncClient):  
    response = await client.get("/user/1")
    body = response.json()
    assert body is not None
      
      
@client_decorator    
async def test_token(client: AsyncClient):
    data = {
        "username": "username",
        "password": "password"
    }
    
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
    