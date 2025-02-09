import pytest
import asyncio
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_user(test_client: TestClient):
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }


    response = test_client.post(url="/user/registr", json=data)
    assert response.status_code == 201