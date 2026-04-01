import pytest
from app.models.user import User

import logging
logger = logging.getLogger(__name__)

import os
adminpassword = os.getenv("MYSQL_PW")

# ------------- Integration Tests -----------------

@pytest.mark.asyncio(loop_scope="session")
async def test_login(client):
    assert await User.username_exists("admin") == True
    user = {"username": "admin", "password": "incorrect"}
    response = await client.post("/auth/login", json=user)
    assert response.status_code == 401

    user = {"username": "admin", "password": adminpassword}
    response = await client.post("/auth/login", json=user)
    assert response.status_code == 200
    results = response.json()
    assert "X-Token" in results

@pytest.mark.asyncio(loop_scope="session")
async def test_get_user(client):
    assert await User.username_exists("admin") == True
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    assert auth.status_code == 200
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/me", headers=auth_header)
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

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/me", headers=auth_header)
    assert response.status_code == 200
    test_user = response.json()
    test_user["firstname"] = "testname"
    test_user["password"] = "newP@ssword"

    response = await client.put("/user", json=test_user, headers=auth_header)
    assert response.status_code == 200
    results = response.json()
    assert results["password"].startswith("$2b$") # password was hashed

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(client):
    assert await User.username_exists("test") == True
    body = {"username": "test", "password": "newP@ssword"}
    auth = await client.post("/auth/login", json=body)
    assert auth.status_code == 200
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/me", headers=auth_header)
    assert response.status_code == 200
    test_user = response.json()
    test_id = test_user["user_id"]

    response = await client.delete(f"/user/{test_id}", headers=auth_header)
    assert response.status_code == 204
    assert await User.username_exists("test") == False

@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_event_id(client):
    response = await client.get("/event/unsafe>>string")
    assert response.status_code == 400
    response = await client.get("/event/doesnotexist")
    assert response.status_code == 404

    response = await client.get("/event?category=Music&limit=1")
    results = response.json()
    for event in results:
        event_id = event["event_id"]
        response = await client.get(f"/event/{event_id}")
        assert response.status_code == 200

@pytest.mark.asyncio(loop_scope="session")
async def test_get_locations(client):
    response = await client.get("/location")
    assert response.status_code == 200
    response = await client.get("/location?limit=3")
    results = response.json()
    assert len(results) == 3

@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_location(client):
    response = await client.get("/location?limit=1")
    locations = response.json()
    for location in locations:
        location_id = location["location_id"]
        response = await client.get(f"/event?location={location_id}")
        assert response.status_code == 200
        results = response.json()
        for event in results:
            assert event["location_id"] == location_id

@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_filter(client):
    response = await client.get("/event?category=M:usic")
    assert response.status_code == 400
    response = await client.get("/event?category=Music")
    assert response.status_code == 200
    response = await client.get("/event?category=Music&limit=3")
    results = response.json()
    assert len(results) == 3

    event = results[0]
    location_id = event["location_id"]
    response = await client.get(f"/event?category=Music&location={location_id}&limit=3")
    assert response.status_code == 200

@pytest.mark.asyncio(loop_scope="session")
async def test_get_location(client):
    response = await client.get("/location?limit=1")
    locations = response.json()
    location = locations[0]
    location_id = location["location_id"]

    response = await client.get(f"/location/{location_id}")
    assert response.status_code == 200
    response = await client.get("/location/doesnotexist")
    assert response.status_code == 404
    response = await client.get("/location/un~safe")
    assert response.status_code == 400

@pytest.mark.asyncio(loop_scope="session")
async def test_post_open_account(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.post("/user/account", headers=auth_header)
    assert response.status_code == 201
    account = response.json()
    assert account["balance"] == 0
    assert account["currency"] == 'USD'

@pytest.mark.asyncio(loop_scope="session")
async def test_get_account(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/account", headers=auth_header)
    assert response.status_code == 200
    account = response.json()
    assert account["balance"] == 0
    assert account["currency"] == 'USD'

@pytest.mark.asyncio(loop_scope="session")
async def test_put_update_balance(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/account", headers=auth_header)
    assert response.status_code == 200
    account = response.json()
    account["balance"] = 50
    account["currency"] = 'GBP'

    response = await client.put("/user/account", json=account, headers=auth_header)
    assert response.status_code == 200
    account = response.json()
    assert account["balance"] == 50
    assert account["currency"] == 'GBP'

@pytest.mark.asyncio(loop_scope="session")
async def test_post_new_booking(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/me", headers=auth_header)
    admin = response.json()

    response = await client.get("/user/account", headers=auth_header)
    account = response.json()

    response = await client.get("/event?limit=1")
    results = response.json()
    event = results[0]

    body = {
        "user_id": admin["user_id"],
        "account_id": account["account_id"],
        "event_id": event["event_id"]
    }

    response = await client.post("/booking", json=body, headers=auth_header)
    assert response.status_code == 201
    booking = response.json()
    assert booking["seats"] == 1
    assert booking["total_price"] == 0

@pytest.mark.asyncio(loop_scope="session")
async def test_get_booking(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/booking", headers=auth_header)
    assert response.status_code == 200
    bookings = response.json()
    booking = bookings[0]
    assert booking["seats"] == 1
    assert booking["total_price"] == 0

@pytest.mark.asyncio(loop_scope="session")
async def test_put_modify_booking(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/booking", headers=auth_header)
    bookings = response.json()
    body = bookings[0]
    body["seats"] = 2
    body["total_price"] = 100

    response = await client.put("/booking", json=body, headers=auth_header)
    assert response.status_code == 200
    booking = response.json()
    assert booking["seats"] == 2
    assert booking["total_price"] == 100

    body["seats"] = 0
    response = await client.put("/booking", json=body, headers=auth_header)
    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_booking(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/booking", headers=auth_header)
    bookings = response.json()
    booking = bookings[0]
    booking_id = booking["booking_id"]

    response = await client.delete(f"/booking/{booking_id}", headers=auth_header)
    assert response.status_code == 204

    response = await client.get("/booking", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []

    response = await client.put("/booking", json=booking, headers=auth_header)
    assert response.status_code == 404

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_account(client):
    user = {"username": "admin", "password": adminpassword}
    auth = await client.post("/auth/login", json=user)
    token_header = auth.json()

    token = token_header["X-Token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/account", headers=auth_header)
    assert response.status_code == 200
    account = response.json()
    account_id = account["account_id"]

    response = await client.delete(f"/user/account/{account_id}", headers=auth_header)
    assert response.status_code == 204

    response = await client.get("/user/account", headers=auth_header)
    assert response.status_code == 404

    response = await client.put("/user/account", json=account, headers=auth_header)
    assert response.status_code == 404





