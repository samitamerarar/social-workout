import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# force TEST in env variable for tests
os.environ["ENV_STATE"] = "test"
from socialworkoutapi.database import database, user_table  # noqa: E402
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


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@email.com", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, registered_user: dict) -> str:
    response = await async_client.post("/token", json=registered_user)
    return response.json()["access_token"]
