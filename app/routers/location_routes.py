from app.models.location import Location
import app.utils as utils
from fastapi import APIRouter, HTTPException

location_router = APIRouter(prefix="/location", tags=["Location"])

@location_router.get("")
async def get_locations(limit: int = 10) -> list[Location]:
    return await Location.list(limit)

@location_router.get(
    "/{location_id}",
    responses = {
        400: { "description": "Bad request" },
        404: { "description": "Event not found" },
    }
)
async def get_location(location_id: str) -> Location:
    if not utils.is_safe_string(location_id, 32):
        raise HTTPException(status_code=400, detail="Unsafe input")
    location = await Location.by_location_id(location_id)
    if location is None:
        raise HTTPException(status_code=404)
    else:
        return location

