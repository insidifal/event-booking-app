from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.timezone_name import TimeZoneName
from datetime import datetime
import app.database as db
from uuid import uuid4
import app.utils as utils

class Location(BaseModel):
    location_id: str = Field(default_factory=lambda: uuid4().hex)
    country: str
    city: str
    timezone: TimeZoneName

    # ------------------- Static Methods -----------------------

    @staticmethod
    async def list(n: int = 10) -> list[Location]:
        """
        n = max number of rows to yield.
        """
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM locations")
                results = await cur.fetchmany(size=n)
                return [Location(
                    location_id=row["location_id"],
                    country=row["country"],
                    city=row["city"],
                    timezone=row["timezone"]
                ) for row in results]

