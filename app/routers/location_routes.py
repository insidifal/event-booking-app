from app.models.location import Location
import app.utils as utils
from fastapi import APIRouter, HTTPException

location_router = APIRouter(prefix="/location", tags=["Location"])

@location_router.get("")
async def get_locations(limit: int = 10) -> list[Location]:
    return await Location.list(limit)

