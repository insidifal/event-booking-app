import pytest
from app.models.user import User

# ------------- Integration Tests -----------------

@pytest.mark.asyncio(loop_scope="session")
async def test_login(client):
    assert await User.username_exists("admin") == True
    body = {"username": "admin", "password": "incorrect"}
    response = await client.post("/auth/login", json=body)
    assert response.status_code == 401
    body = {"username": "admin", "password": "changeme"}
    response = await client.post("/auth/login", json=body)
    assert response.status_code == 200
    results = response.json()
    assert "X-Token" in results

@pytest.mark.asyncio(loop_scope="session")
async def test_get_user(client):
    assert await User.username_exists("admin") == True
    body = {"username": "admin", "password": "changeme"}
    auth = await client.post("/auth/login", json=body)
    assert auth.status_code == 200
    token_header = auth.json()
    response = await client.get("/user/me", headers=token_header)
    assert response.status_code == 200
    response = await client.get("/user/me")
    assert response.status_code == 401

@pytest.mark.asyncio(loop_scope="session")
async def test_post_add_user(client):
    test_user = {
        "username": "test",
        "firstname": "test",
        "lastname": "test",
    }
    response = await client.post("/user", json=test_user)
    assert response.status_code == 201
    results = response.json()
    assert results["user_id"] is not None

@pytest.mark.asyncio(loop_scope="session")
async def test_post_modify_user(client):
    assert await User.username_exists("test") == True
    body = {"username": "test"}
    auth = await client.post("/auth/login", json=body)
    assert auth.status_code == 200
    token_header = auth.json()

    response = await client.get("/user/me", headers=token_header)
    assert response.status_code == 200
    test_user = response.json()
    test_user["firstname"] = "testname"
    test_user["password"] = "newP@ssword"

    response = await client.put("/user", json=test_user, headers=token_header)
    assert response.status_code == 200
    results = response.json()
    assert results["password"].startswith("$2b$")

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(client):
    assert await User.username_exists("test") == True
    body = {"username": "test", "password": "newP@ssword"}
    auth = await client.post("/auth/login", json=body)
    assert auth.status_code == 200
    token_header = auth.json()

    response = await client.get("/user/me", headers=token_header)
    assert response.status_code == 200
    test_user = response.json()
    test_id = test_user["user_id"]

    response = await client.delete(f"/user/{test_id}", headers=token_header)
    assert response.status_code == 204
    assert await User.username_exists("test") == False

