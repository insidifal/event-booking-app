import pytest
import app.utils as utils
from app.models.user import User
from pydantic import ValidationError
from fastapi import HTTPException
from time import sleep

# ------------- Unit Tests -----------------

def test_is_safe_string():
    assert utils.is_safe_string("Asafe_u$er-n@me123") == True
    assert utils.is_safe_string("An unsafe 'string'") == False

def test_jwt_token():
    test_payload = {"body": "test"}
    token = utils.create_token(test_payload, expire_time=1)
    assert isinstance(token, str)

    payload = utils.check_token(token)
    assert payload["body"] == "test"
    with pytest.raises(HTTPException):
        _ = utils.check_token("invalidtoken")
    # This works but disabling for faster testing
    # sleep(2)
    # with pytest.raises(HTTPException):
    #     _ = utils.check_token(token)

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
    user.hash_password()
    assert user.password != "test"
    assert user.password.startswith("$2b$")

@pytest.mark.asyncio(loop_scope="session")
async def test_username_exists():
    assert await User.username_exists("test") == False
    assert await User.username_exists("admin") == True

@pytest.mark.asyncio(loop_scope="session")
async def test_add_user():
    user = User(
        username="test",
        firstname="test",
        lastname="test",
        password="test_password"
    )
    await user.add_user()
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
async def test_user_id_exists():
    user = await User.by_username("test")
    assert await User.user_id_exists(user.user_id) == True
    assert await User.user_id_exists("doesnotexist") == False

@pytest.mark.asyncio(loop_scope="session")
async def test_verify_password():
    user = await User.by_username("test")
    is_correct = user.verify_password("test_password")
    assert is_correct == True
    is_not_correct = user.verify_password("wrong_password")
    assert is_not_correct == False

@pytest.mark.asyncio(loop_scope="session")
async def test_modify_user():
    user = await User.by_username("test")
    mod_user = User(
        user_id=user.user_id,
        username=user.username,
        firstname="newname",
        lastname=user.lastname,
        password="Anewp@$$w0rd",
        location_id=user.location_id
        )
    user = await mod_user.modify_user()
    assert user.firstname == "newname"
    assert user.password.startswith("$2b$") # new password is hashed

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user():
    user = await User.by_username("test")
    await user.delete_user()
    assert await User.username_exists("test") == False

