import os
import pytest
import anyio
from fastapi.testclient import TestClient

# A fixture provides a defined, reliable and
# consistent context for the tests.

@pytest.fixture(scope="session", autouse=True)
def set_environ():
    os.environ["APP_ENV"] = "testing"

@pytest.fixture
def api_key():
    return os.getenv("EVENTBRITE_TOKEN")

@pytest.fixture
def client():
    from app.main import app
    with TestClient(app) as testclient:
        yield testclient

# ------------- Integration Tests -----------------

def test_get_user_with_token(client, api_key):
    headers = { "X-Token": api_key }
    response = client.get("/user/login", headers=headers)
    assert response.status_code == 200
    results = response.json()
    assert 'user_id' in results
    assert 'firstname' in results
    assert 'lastname' in results
