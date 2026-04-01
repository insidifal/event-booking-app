from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.currency_code import Currency
import app.database as db
from uuid import uuid4
import app.utils as utils

class Booking(BaseModel):
    booking_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: str
    account_id: str
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
                booking = Booking.model_validate(self) # applies types and input validation
                # Update the booked seats in events
                sql = """
                    UPDATE events SET booked = booked + %s
                    WHERE event_id = %s
                    """
                values = (self.seats, self.event_id)
                await cur.execute(sql, values)
                # Insert booking record
                sql = """
                    INSERT INTO bookings (booking_id, user_id, account_id, event_id, seats, total_price, currency)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                values = (self.booking_id, self.user_id, self.account_id, self.event_id, self.seats, self.total_price, self.currency)
                await cur.execute(sql, values)
                # Insert transaction record
                sql = """
                    INSERT INTO transactions (transaction_id, booking_id, account_id, amount, currency)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                values = (uuid4().hex, self.booking_id, self.account_id, self.total_price, self.currency)
                await cur.execute(sql, values)
                # Update the account balance
                sql = """
                    UPDATE accounts SET balance = balance - %s
                    WHERE account_id = %s
                    """
                values = (self.total_price, self.account_id)
                await cur.execute(sql, values)
                return self

    async def modify_booking(self) -> Booking:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                booking = Booking.model_validate(self) # applies types and input validation
                original = await Booking.by_booking_id(self.booking_id)
                if original is None:
                    return None # booking_id does not exist so do not proceed with other changes
                # Updates the number of seats in the event
                price_change = self.total_price - original.total_price
                sql = """
                    UPDATE events SET booked = booked - %s + %s
                    WHERE event_id = %s
                    """
                values = (original.seats, self.seats, self.event_id)
                await cur.execute(sql, values)
                # Update the booking details
                sql = """
                    UPDATE bookings SET seats = %s, total_price = %s, currency = %s
                    WHERE booking_id = %s
                    """
                values = (self.seats, self.total_price, self.currency, self.booking_id)
                await cur.execute(sql, values)
                # Insert transaction record
                sql = """
                    INSERT INTO transactions (transaction_id, booking_id, account_id, amount, currency)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                values = (uuid4().hex, self.booking_id, self.account_id, price_change, self.currency)
                await cur.execute(sql, values)
                # Update the account balance
                sql = """
                    UPDATE accounts SET balance = balance - %s
                    WHERE account_id = %s
                    """
                values = (price_change, self.account_id)
                await cur.execute(sql, values)
                return self

    async def cancel_booking(self):
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                booking = Booking.model_validate(self) # applies types and input validation
                # Updates the number of seats in the event
                sql = """
                    UPDATE events SET booked = booked - %s
                    WHERE event_id = %s
                    """
                values = (self.seats, self.event_id)
                await cur.execute(sql, values)
                # Delete the booking
                await cur.execute("DELETE FROM bookings WHERE booking_id = %s", self.booking_id)
                # Insert transaction record
                sql = """
                    INSERT INTO transactions (transaction_id, booking_id, account_id, amount, currency)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                values = (uuid4().hex, self.booking_id, self.account_id, -self.total_price, self.currency)
                await cur.execute(sql, values)
                # Update the account balance
                sql = """
                    UPDATE accounts SET balance = balance + %s
                    WHERE account_id = %s
                    """
                values = (self.total_price, self.account_id)
                await cur.execute(sql, values)

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
                        account_id=results["account_id"],
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
                        account_id=row["account_id"],
                        event_id=row["event_id"],
                        seats=row["seats"],
                        total_price=row["total_price"],
                        currency=row["currency"]
                    ) for row in results]
                else:
                    return []

