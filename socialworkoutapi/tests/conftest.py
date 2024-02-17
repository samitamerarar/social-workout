import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# force TEST in env variable for tests
os.environ["ENV_STATE"] = "test"
from socialworkoutapi.database import database  # noqa: E402
from socialworkoutapi.main import app  # noqa: E402


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
    await database.connect()
    yield
    await database.disconnect()  # this rollback database in database config


@pytest.fixture()  # Dependency injection (client param runs the client() function)
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as asynclient:
        yield asynclient
