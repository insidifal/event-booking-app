from app.models.event import Event
import app.utils as utils
from fastapi import APIRouter, Header, status, HTTPException
from typing import Annotated

event_router = APIRouter(prefix="/event", tags=["Event"])

@event_router.get(
    "/{event_id}",
    responses = {
        400: { "description": "Bad request" },
        404: { "description": "Event not found" },
        500: { "description": "Internal server error" },
    }
)
async def get_event(event_id: str) -> Event:
    if not utils.is_safe_string(event_id, 50):
        raise HTTPException(status_code=400, detail="Unsafe input")
    if not await Event.event_id_exists(event_id):
        raise HTTPException(status_code=404)
    try:
        return await Event.by_event_id(event_id)
    except:
        raise HTTPException(status_code=500)

@event_router.get(
    "",
    responses = {
        400: { "description": "Bad request" },
        500: { "description": "Internal server error" },
    }
)
async def get_by_category(category: str, limit: int = 10) -> list[Event]:
    if not utils.is_safe_string(category):
        raise HTTPException(status_code=400, detail="Unsafe input")
    try:
        return await Event.by_category(category, limit)
    except:
        raise HTTPException(status_code=500)

