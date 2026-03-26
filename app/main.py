import os
import app.routers as routers
from fastapi import FastAPI

app = FastAPI()

if os.getenv("APP_ENV") == "testing":
    app.include_router(routers.test_router)

app.include_router(routers.main_router)


