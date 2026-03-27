from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.timezone_name import TimeZoneName
from pydantic_extra_types.currency_code import Currency
import app.database as db
from uuid import uuid4
import bcrypt
import app.utils as utils

class User(BaseModel):
    # Automatically generates a unique ID
    user_id: str = Field(default_factory=lambda: uuid4().hex)
    username: str
    firstname: str
    lastname: str
    password: str | None = None
    location_id: str | None = None

    @model_validator(mode='after')
    def validate_input(self) -> User:
        if not utils.is_safe_string(self.username) or len(self.username) > 15:
            raise ValueError("Unsafe username")
        if not utils.is_safe_string(self.firstname) or len(self.firstname) > 15:
            raise ValueError("Unsafe firstname")
        if not utils.is_safe_string(self.lastname) or len(self.lastname) > 15:
            raise ValueError("Unsafe lastname")
        return self

    @model_validator(mode='after')
    def hash_password(self) -> User:
        """
        Password hashing triggers automatically when instantiating a new User
        """
        if self.password is not None:
            if not self.password.startswith("$2b$"):
                # Prevent double hashing
                _password = self.password.encode('utf-8')
                _hashed = bcrypt.hashpw(_password, bcrypt.gensalt())
                self.password = _hashed.decode('utf-8')
        return self

    def verify_password(self, password: str) -> bool:
        _password = password.encode('utf-8')
        pw_stored = self.password.encode('utf-8')
        check = bcrypt.checkpw(_password, pw_stored)
        return check

    async def delete_user(self):
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("DELETE FROM users WHERE user_id = %s", self.user_id)
                except:
                    raise Exception("Could not delete user")

    # ------------------- Static Methods -----------------------

    @staticmethod
    async def username_exists(username: str) -> bool:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("SELECT 1 FROM users WHERE username = %s", username)
                    return cur.rowcount > 0
                except:
                    raise Exception("Could not search for username")

    @staticmethod
    async def new_user(username, firstname, lastname, password) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    new_user = User(
                        username=username,
                        firstname=firstname,
                        lastname=lastname,
                        password=password # password will be hashed here
                    )
                    # Pydantic will raise validation errors here to be handled in the router
                    sql = """
                        INSERT INTO users (user_id, username, firstname, lastname, password)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                    values = (new_user.user_id, new_user.username, new_user.firstname, new_user.lastname, new_user.password)
                    await cur.execute(sql, values)
                    return new_user
                except:
                    raise Exception("Could not create user")

    @staticmethod
    async def by_username(username: str) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("SELECT * FROM users WHERE username = %s", username)
                    results = await cur.fetchone()
                    return User(
                        user_id=results["user_id"],
                        username=results["username"],
                        firstname=results["firstname"],
                        lastname=results["lastname"],
                        password=results["password"],
                        location_id=results["location_id"]
                    )
                except:
                    raise Exception("Could not retieve user")

