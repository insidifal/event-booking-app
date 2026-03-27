from app.models.user import User
from typing import Annotated
from fastapi import APIRouter, Header, HTTPException

main_router = APIRouter()
test_router = APIRouter(prefix="/tests", tags=["Tests"])
