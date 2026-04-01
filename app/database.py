import os
import aiomysql
from pymysql.constants import CLIENT

import logging
logger = logging.getLogger(__name__)

# Pool for asynchronous database connections
pool = None

async def get_database_pool():
    host = os.getenv("DB_HOST", "localhost")
    password = os.getenv("MYSQL_PW")
    global pool
    if pool is None:
        pool = await aiomysql.create_pool(
            host=host,
            port=3306,
            user="root",
            password=password,
            db="events_booking_app",
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

