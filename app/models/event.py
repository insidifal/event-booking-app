from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.currency_code import Currency
from datetime import datetime
import app.database as db
from uuid import uuid4
import app.utils as utils

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    description: str
    capacity: int
    booked: int
    start: datetime
    end: datetime
    location_id: str | None = None
    category: str
    price: float
    currency: Currency

    @model_validator(mode='after')
    def validate_input(self) -> User:
        if not utils.is_safe_string(self.name, 30):
            raise ValueError("Unsafe event name")
        if not utils.is_safe_string(self.description, 100):
            raise ValueError("Unsafe description")
        if not utils.is_safe_string(self.category):
            raise ValueError("Unsafe category")

        if self.booked < 0:
            raise ValueError("Booked seats must be non-negative")
        if self.capacity <= 0:
            raise ValueError("Capacity must be greater than zero")
        if self.booked > self.capacity:
            raise ValueError("Booked seats exceeds capacity")

        if self.end < self.start:
            raise ValueError("End time must be after start time")

        return self

    async def modify_event(self) -> Event:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                event = Event.model_validate(self) # applies types and input validation
                sql = """
                    UPDATE events SET name = %s, description = %s, capacity = %s, booked = %s, start = %s, end = %s, location_id = %s, category = %s, price = %s, currency = %s
                    WHERE event_id = %s
                    """
                values = (self.name, self.description, self.capacity, self.booked, self.start, self.end, self.location_id, self.category, self.price, self.currency, self.event_id)
                await cur.execute(sql, values)
                return self

    # ------------------- Static Methods -----------------------

    @staticmethod
    async def event_id_exists(event_id: str) -> bool:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1 FROM events WHERE event_id = %s", event_id)
                return cur.rowcount > 0

    @staticmethod
    async def by_category(category: str, n: int = 10) -> list[Event]:
        """
        Returns a generator that yields an event_id in the specified category.
        n = max number of rows to yield.
        """
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM events WHERE category = %s", category)
                results = await cur.fetchmany(size=n)
                return [Event(
                    event_id=row["event_id"],
                    name=row["name"],
                    description=row["description"],
                    capacity=row["capacity"],
                    booked=row["booked"],
                    start=row["start"],
                    end=row["end"],
                    location_id=row["location_id"],
                    category=row["category"],
                    price=row["price"],
                    currency=row["currency"]
                ) for row in results]


    @staticmethod
    async def by_event_id(event_id: str) -> Event:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM events WHERE event_id = %s", event_id)
                results = await cur.fetchone()
                return Event(
                    event_id=results["event_id"],
                    name=results["name"],
                    description=results["description"],
                    capacity=results["capacity"],
                    booked=results["booked"],
                    start=results["start"],
                    end=results["end"],
                    location_id=results["location_id"],
                    category=results["category"],
                    price=results["price"],
                    currency=results["currency"]
                )

