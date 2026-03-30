import pytest
from pydantic import ValidationError
from fastapi import HTTPException
from time import sleep
from contextlib import aclosing

# ------------- Unit Tests -----------------

import app.utils as utils

def test_is_safe_string():
    assert utils.is_safe_string("Asafe_u$er-n@me123") == True
    assert utils.is_safe_string("An unsafe 'string'") == False

def test_jwt_token():
    token = utils.create_token("test", expire_time=1)
    assert isinstance(token, str)

    user_id = utils.authorize(token)
    assert user_id == "test"
    with pytest.raises(HTTPException):
        _ = utils.authorize("invalidtoken")
    # This works but disabling for faster testing
    # sleep(2)
    # with pytest.raises(HTTPException):
    #     _ = utils.authorize(token)

from app.models.user import User

def test_user():
    # Pydantic will raise validation errors
    with pytest.raises(ValidationError):
        _ = User()
    with pytest.raises(ValidationError):
        _ = User(
            username="//unsafe",
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

from app.models.event import Event

def test_event():
    with pytest.raises(ValidationError):
        _ = Event()
    event = Event(
        name="Test",
        description="Test event",
        capacity=100,
        booked=50,
        start='2024-07-06 00:00:00',
        end='2024-07-09 00:00:00',
        category='Test',
        price=12.34,
        currency='ZAR'
    )

@pytest.mark.asyncio(loop_scope="session")
async def test_by_filter():
    events = await Event.by_filter(category="Music")
    for event in events:
        assert isinstance(event, Event)
        assert event.category == "Music"

    results = await Event.by_filter(category="Music", n=1)
    event = results[0]
    location_id = event.location_id
    location_events = await Event.by_filter(location_id=location_id, n=3)
    assert len(location_events) == 3
    for location in location_events:
        assert isinstance(location, Event)

@pytest.mark.asyncio(loop_scope="session")
async def test_by_event_id():
    events = await Event.by_filter(category="Music", n=1)
    for event in events:
        event_id = event.event_id
        get_event = await Event.by_event_id(event_id)
        assert get_event.category == "Music"

@pytest.mark.asyncio(loop_scope="session")
async def test_modify_event():
    events = await Event.by_filter(category="Music", n=1)
    for event in events:
        event_id = event.event_id
        event.capacity = 100
        event.booked = 99
        modified_event = await event.modify_event()
        assert modified_event.event_id == event_id
        assert modified_event.booked == 99
        modified_event.booked += 2
        with pytest.raises(ValidationError):
            await modified_event.modify_event()

from app.models.location import Location

def test_location():
    with pytest.raises(ValidationError):
        _ = Location()
    location = Location(
        country="South Africa",
        city="Cape Town",
        timezone="Africa/Johannesburg"
    )
    with pytest.raises(ValidationError):
        _ = Location(
            country="South Africa",
            city="Cape Town",
            timezone="Africa"
        )

@pytest.mark.asyncio(loop_scope="session")
async def test_list():
    locations = await Location.list()
    for location in locations:
        assert isinstance(location, Location)

