from pydantic import BaseModel
from pydantic_extra_types.timezone_name import TimeZoneName
from pydantic_extra_types.currency_code import Currency

import app.service as srv

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class User(BaseModel):
    user_id: str
    firstname: str
    lastname: str
    token: str
    country: str | None
    city: str | None
    timezone: TimeZoneName | None
    currency: Currency | None

    @staticmethod
    async def login(auth_token: str) -> User:
        try:
            user = await srv.get_eventbrite_user(auth_token)
        except Exception as e:
            logging.error(e)
            return None
        else:
            return User(
                user_id=user['id'],
                firstname=user['first_name'],
                lastname=user['last_name'],
                token=auth_token, # encrypt
                country=None,
                city=None,
                timezone=None,
                currency=None
            )

