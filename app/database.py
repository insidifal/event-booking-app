import os
import aiomysql
from pymysql.constants import CLIENT

import logging
logger = logging.getLogger(__name__)

# Pool for asynchronous database connections
pool = None

async def get_database_pool():
    global pool
    if pool is None:
        pool = await aiomysql.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("MYSQL_PW"),
            db=os.getenv("DATABASE"),
            autocommit=True,
            cursorclass=aiomysql.DictCursor,
            client_flag=CLIENT.FOUND_ROWS
        )
        logger.info("Connected to database")
    return pool

async def close_pool():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        logger.info("Closed connection to database")
        pool = None

