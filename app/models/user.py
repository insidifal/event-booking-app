from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.timezone_name import TimeZoneName
from pydantic_extra_types.currency_code import Currency
import app.database as db
from uuid import uuid4
import bcrypt

class User(BaseModel):
    # Automatically generates a unique ID
    user_id: str = Field(default_factory=lambda: uuid4().hex)
    username: str
    firstname: str
    lastname: str
    password: str
    location_id: str | None = None

    @model_validator(mode='after')
    def hash_password(self) -> User:
        """
        Password hashing triggers automatically when instantiating a new User
        """
        if not self.password.startswith("$2b$"):
            # Prevent double hashing
            _password = self.password.encode('utf-8')
            _hashed = bcrypt.hashpw(_password, bcrypt.gensalt())
            self.password = _hashed.decode('utf-8')
        return self

    @staticmethod
    async def username_exists(username: str) -> bool:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1 FROM users WHERE username = %s", username)
                return cur.rowcount > 0

    @staticmethod
    async def new_user(username, firstname, lastname, password) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
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

    @staticmethod
    async def get_by_username(username: str) -> User:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
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

    async def delete_user(self):
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM users WHERE user_id = %s", self.user_id)

    def verify_password(password: str) -> bool:
        ...
