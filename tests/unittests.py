import pytest
import app.utils as utils
from app.models.user import User
from pydantic import ValidationError

# ------------- Unit Tests -----------------

def test_user():
    # Pydantic will raise validation errors
    with pytest.raises(ValidationError):
        _ = User()
    with pytest.raises(ValidationError):
        _ = User(
            username="  unsafe  ",
            firstname="test",
            lastname="test"
        )
    _ = User(
        username="test",
        firstname="test",
        lastname="test"
    )
    user = User(
        username="test",
        firstname="test",
        lastname="test",
        password="test"
    )
    # validate password hashing
    assert user.password != "test"
    assert user.password.startswith("$2b$")

def test_is_safe_string():
    assert utils.is_safe_string("Asafe_u$er-n@me123") == True
    assert utils.is_safe_string("An unsafe 'string'") == False

@pytest.mark.asyncio(loop_scope="session")
async def test_username_exists():
    assert await User.username_exists("test") == False
    assert await User.username_exists("admin") == True

@pytest.mark.asyncio(loop_scope="session")
async def test_new_user():
    user = await User.new_user(
        username="test",
        firstname="test",
        lastname="test",
        password="test_password"
    )
    assert await User.username_exists("test") == True

@pytest.mark.asyncio(loop_scope="session")
async def test_by_username():
    user = await User.by_username("test")
    assert user.username == "test"
    with pytest.raises(Exception):
        _ = await User.by_username("doesnotexist")
    admin = await User.by_username("admin")
    assert admin.username == "admin"

@pytest.mark.asyncio(loop_scope="session")
async def test_verify_password():
    user = await User.by_username("test")
    is_correct = user.verify_password("test_password")
    assert is_correct == True
    is_not_correct = user.verify_password("wrong_password")
    assert is_not_correct == False

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user():
    user = await User.by_username("test")
    await user.delete_user()
    assert await User.username_exists("test") == False

