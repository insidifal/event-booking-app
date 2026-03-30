from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.currency_code import Currency
import app.database as db
from uuid import uuid4
import app.utils as utils

class Account(BaseModel):
    account_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: str
    balance: float = Field(default_factory=lambda: 0)
    currency: Currency = Field(default_factory=lambda: 'USD')

    @model_validator(mode='after')
    def validate_input(self) -> Account:
        if self.balance < 0:
            raise ValueError("Cannot have negative balance")
        return self

    async def open(self) -> Account:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Pydantic will raise validation errors here to be handled in the router
                sql = """
                    INSERT INTO accounts (account_id, user_id, balance, currency)
                    VALUES (%s, %s, %s, %s)
                    """
                values = (self.account_id, self.user_id, self.balance, self.currency)
                await cur.execute(sql, values)
                return self

    async def update_balance(self) -> Account:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                account = Account.model_validate(self) # applies types and input validation
                sql = """
                    UPDATE accounts SET balance = %s, currency = %s
                    WHERE account_id = %s
                    """
                values = (self.balance, self.currency, self.account_id)
                await cur.execute(sql, values)
                return self

    async def delete_account(self):
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM accounts WHERE account_id = %s", self.account_id)

    # ------------------- Static Methods -----------------------

    @staticmethod
    async def by_user_id(user_id: str) -> Account | None:
        pool = await db.get_database_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM accounts WHERE user_id = %s", user_id)
                results = await cur.fetchone()
                # fetches first account for user - technically they could have more than one
                if cur.rowcount > 0:
                    return Account(
                        account_id=results["account_id"],
                        user_id=results["user_id"],
                        balance=results["balance"],
                        currency=results["currency"]
                    )
                else:
                    return None

