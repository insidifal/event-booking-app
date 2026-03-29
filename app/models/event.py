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

    # ------------------- Static Methods -----------------------

    @staticmethod
    async def event_id_exists(event_id: str) -> bool:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("SELECT 1 FROM events WHERE event_id = %s", event_id)
                    return cur.rowcount > 0
                except:
                    raise Exception("Could not search for event ID")

    @staticmethod
    async def by_category(category: str, n: int = 10) -> Event:
        """
        Returns a generator that yields an event_id in the specified category.
        n = max number of rows to yield.
        """
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("SELECT * FROM events WHERE category = %s", category)
                    results = await cur.fetchmany(size=n)
                    return results
                except:
                    raise Exception("Could not retieve event")

    @staticmethod
    async def by_event_id(event_id: str) -> Event:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
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
                except:
                    raise Exception("Could not retieve event")

