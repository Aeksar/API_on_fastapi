import pytest
from httpx import AsyncClient

from tests.test_endpoints.setup_tests import get_test_session, client_decorator


@client_decorator
async def test_get_all_task(client: AsyncClient):
    response = await client.get(url="/task/all")
    task_list = response.json()
    assert response.status_code == 200