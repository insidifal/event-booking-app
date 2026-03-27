import pytest
from app.models.user import User

# ------------- Integration Tests -----------------

@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_username(client):
    assert await User.username_exists("test") == False
    response = await client.get("/user?username=test")
    assert response.status_code == 404

    assert await User.username_exists("admin") == True
    response = await client.get("/user?username=admin")
    assert response.status_code == 200
