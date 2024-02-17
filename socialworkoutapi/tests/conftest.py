from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from socialworkoutapi.main import app
from socialworkoutapi.routers.post import comment_table, post_table


# Shared accross other tests
@pytest.fixture(scope="session")  # runs once for theentire test session
def anyio_backend():
    return "asyncio"  # built-in framework


# Shared accross other tests
@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


# Shared accross other tests
@pytest.fixture(autouse=True)  # runs on every test
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()  # Dependency injection (client param runs the client() function)
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as asynclient:
        yield asynclient
