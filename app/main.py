import os
import app.database as db
from app.routers.user_routes import user_router
from app.routers.auth import auth_router
from fastapi import FastAPI
from contextlib import asynccontextmanager

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# ------------ Database Connection ---------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan of the app to handle the database connection.
    Keeps the database connection open.
    Replaces deprecated event_on.
    """
    await db.get_database_pool() # Starts connection to database
    yield
    await db.close_pool() # Close connection

# --------------- Application -----------------

app = FastAPI(lifespan=lifespan)

if os.getenv("APP_ENV") == "testing":
    app.include_router(routers.test_router)

app.include_router(user_router)
app.include_router(auth_router)

