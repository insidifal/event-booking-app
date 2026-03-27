import pytest
from app.models.user import User
from pydantic import ValidationError

# ------------- Unit Tests -----------------

def test_user():
    # Pydantic will raise validation errors
    with pytest.raises(ValidationError):
        _ = User()
    user = User(
        username="test",
        firstname="test",
        lastname="test",
        password="test"
    )
    # validate password hashing
    assert user.password != "test"
    assert user.password.startswith("$2b$")

@pytest.mark.asyncio(loop_scope="session")
async def test_username_exists():
    assert await User.username_exists("test") == False

@pytest.mark.asyncio(loop_scope="session")
async def test_new_user():
    user = await User.new_user(
        username="test",
        firstname="test",
        lastname="test",
        password="test"
    )
    assert await User.username_exists("test") == True

@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_username():
    user = await User.get_by_username("test")
    assert user.username == "test"

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user():
    user = await User.get_by_username("test")
    await user.delete_user()
    assert await User.username_exists("test") == False

