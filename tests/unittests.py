import os
import pytest
import anyio
import app.service as srv
import app.model as model

@pytest.fixture(scope="session", autouse=True)
def set_environ():
    os.environ["APP_ENV"] = "testing"

@pytest.fixture
def api_key():
    return os.getenv("EVENTBRITE_TOKEN")

def test_get_eventbrite_token(api_key):
    assert isinstance(api_key, str)

@pytest.mark.anyio
async def test_get_eventbrite_user(api_key):
    with pytest.raises(TypeError):
        _ = await srv.get_eventbrite_user(None)

    user = await srv.get_eventbrite_user(api_key)
    assert isinstance(user, dict)
    assert 'id' in user
    assert 'first_name' in user
    assert 'last_name' in user

def test_new_user():
    # Pydantic will raise validation errors
    new_user = model.User(
        user_id="test",
        firstname="test",
        lastname="test",
        token="test",
        country=None,
        city=None,
        timezone=None,
        currency=None
    )

@pytest.mark.anyio
async def test_user_login(api_key):
    user = await model.User.login(None)
    assert user == None # exception handled successfully

    user = await model.User.login(api_key)
    assert user.token == api_key
    assert user.firstname == "Joshua"
    assert user.lastname == "Marks"

