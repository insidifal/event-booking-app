import os
from datetime import datetime
import app.database as db
from app.routers.auth import auth_router
from app.routers.user_routes import user_router
from app.routers.event_routes import event_router
from app.routers.location_routes import location_router
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

# ------------------- Logging ----------------------

import logging
from pythonjsonlogger import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = json.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)

# ------------------- Paths ----------------------

app_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(app_dir)
static_dir = os.path.join(base_dir, "public/static")
templates_dir = os.path.join(base_dir, "public/templates")
favicon_file = os.path.join(static_dir, "favicon.ico")

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

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(event_router)
app.include_router(location_router)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_file)

