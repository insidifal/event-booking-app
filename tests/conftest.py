import os
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
import app.database as db
from app.main import app

# A fixture provides a defined, reliable and
# consistent context for the tests.

@pytest.fixture(scope="session", autouse=True)
def set_environ():
    """
    Sets the environment to "testing".
    """
    os.environ["APP_ENV"] = "testing"

@pytest.fixture(scope="session")
def event_loop():
    """
    A single event loop to span multiple tests.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def pool(event_loop):
    """
    Handles the database connection pool lifecycle.
    """
    yield await db.get_database_pool()
    await db.close_pool()

@pytest.fixture
async def client():
    """
    An asynchronous test client.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as testclient:
        yield testclient


