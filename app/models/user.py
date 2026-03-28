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
    firstname: str | None = None
    lastname: str | None = None
    password: str | None = None
    location_id: str | None = None

    @model_validator(mode='after')
    def validate_input(self) -> User:
        if not utils.is_safe_string(self.username):
            raise ValueError("Unsafe username")
        if not utils.is_safe_string(self.firstname):
            raise ValueError("Unsafe firstname")
        if not utils.is_safe_string(self.lastname):
            raise ValueError("Unsafe lastname")
        return self

    def hash_password(self):
        if self.password is not None:
            if not self.password.startswith("$2b$"):
                # Prevent double hashing
                _password = self.password.encode('utf-8')
                _hashed = bcrypt.hashpw(_password, bcrypt.gensalt())
                self.password = _hashed.decode('utf-8')

    def verify_password(self, password: str) -> bool:
        if password is None and self.password is None:
            return True
        elif password is not None and self.password is None:
            return False
        elif password is None and self.password is not None:
            return False
        _password = password.encode('utf-8')
        pw_stored = self.password.encode('utf-8')
        check = bcrypt.checkpw(_password, pw_stored)
        return check

    async def add_user(self) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    # Pydantic will raise validation errors here to be handled in the router
                    self.hash_password()
                    sql = """
                        INSERT INTO users (user_id, username, firstname, lastname, password)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                    values = (self.user_id, self.username, self.firstname, self.lastname, self.password)
                    await cur.execute(sql, values)
                    return self
                except:
                    raise Exception("Could not create user")

    async def modify_user(self) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    self.hash_password()
                    sql = """
                        UPDATE users SET firstname = %s, lastname = %s, password = %s, location_id = %s
                        WHERE user_id = %s
                        """
                    values = (self.firstname, self.lastname, self.password, self.location_id, self.user_id)
                    await cur.execute(sql, values)
                    return self
                except:
                    raise Exception("Could not modify user")

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
    async def user_id_exists(user_id: str) -> bool:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("SELECT 1 FROM users WHERE user_id = %s", user_id)
                    return cur.rowcount > 0
                except:
                    raise Exception("Could not search for user ID")

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

    @staticmethod
    async def by_user_id(user_id: str) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("SELECT * FROM users WHERE user_id = %s", user_id)
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

