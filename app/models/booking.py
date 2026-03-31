from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.currency_code import Currency
import app.database as db
from uuid import uuid4
import app.utils as utils

class Booking(BaseModel):
    booking_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: str
    event_id: str
    seats: int = Field(default_factory=lambda: 1)
    total_price: float = Field(default_factory=lambda: 0)
    currency: Currency = Field(default_factory=lambda: 'USD')

    @model_validator(mode='after')
    def validate_input(self) -> Booking:
        if self.seats < 1:
            raise ValueError("Must be one or more seats")
        if self.total_price < 0:
            raise ValueError("Price cannot be negative")
        return self

    async def new_booking(self) -> Booking:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Pydantic will raise validation errors here to be handled in the router
                sql = """
                    UPDATE events SET booked = booked + %s
                    WHERE event_id = %s
                    """
                values = (self.seats, self.event_id)
                await cur.execute(sql, values)
                sql = """
                    INSERT INTO bookings (booking_id, user_id, event_id, seats, total_price, currency)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                values = (self.booking_id, self.user_id, self.event_id, self.seats, self.total_price, self.currency)
                await cur.execute(sql, values)
                return self

    async def modify_booking(self) -> Booking:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                booking = Booking.model_validate(self) # applies types and input validation
                sql = """
                    UPDATE events SET booked = booked - (SELECT seats FROM bookings WHERE booking_id = %s) + %s
                    WHERE event_id = %s
                    """
                values = (self.booking_id, self.seats, self.event_id)
                await cur.execute(sql, values)
                sql = """
                    UPDATE bookings SET seats = %s, total_price = %s, currency = %s
                    WHERE booking_id = %s
                    """
                values = (self.seats, self.total_price, self.currency, self.booking_id)
                await cur.execute(sql, values)
                if cur.rowcount > 0:
                    return self
                else:
                    return

    async def cancel_booking(self):
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = """
                    UPDATE events SET booked = booked - %s
                    WHERE event_id = %s
                    """
                values = (self.seats, self.event_id)
                await cur.execute(sql, values)
                await cur.execute("DELETE FROM bookings WHERE booking_id = %s", self.booking_id)

    # ------------------- Static Methods -----------------------

    @staticmethod
    async def by_booking_id(booking_id: str) -> Booking | None:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM bookings WHERE booking_id = %s", booking_id)
                results = await cur.fetchone()
                if cur.rowcount > 0:
                    return Booking(
                        booking_id=results["booking_id"],
                        user_id=results["user_id"],
                        event_id=results["event_id"],
                        seats=results["seats"],
                        total_price=results["total_price"],
                        currency=results["currency"]
                    )
                else:
                    return None

    @staticmethod
    async def by_user_id(user_id: str, n: int = 10) -> list[Booking]:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM bookings WHERE user_id = %s", user_id)
                results = await cur.fetchmany(size=n)
                if cur.rowcount > 0:
                    return [Booking(
                        booking_id=row["booking_id"],
                        user_id=row["user_id"],
                        event_id=row["event_id"],
                        seats=row["seats"],
                        total_price=row["total_price"],
                        currency=row["currency"]
                    ) for row in results]
                else:
                    return []

