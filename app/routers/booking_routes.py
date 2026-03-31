from app.models.booking import Booking
import app.utils as utils
from fastapi import APIRouter, Header, status, HTTPException
from typing import Annotated

booking_router = APIRouter(prefix="/booking", tags=["Booking"])

@booking_router.get(
    "",
    responses = {
        401: { "description": "Unauthorized" },
    }
)
async def get_bookings(authorization: Annotated[str | None, Header()] = None) -> list[Booking]:
    user_id = utils.authorize(authorization) # raises HTTPException
    return await Booking.by_user_id(user_id)

@booking_router.post(
    "", status_code=status.HTTP_201_CREATED,
    responses = {
        401: { "description": "Unauthorized" },
        409: { "description": "Booking already exists" },
    }
)
async def post_new_booking(booking: Booking, authorization: Annotated[str | None, Header()] = None) -> Booking:
    user_id = utils.authorize(authorization) # raises HTTPException
    if await Booking.by_booking_id(booking.booking_id) is None:
        return await booking.new_booking()
    else:
        raise HTTPException(status_code=409)

@booking_router.put(
    "",
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "Booking not found" },
    }
)
async def put_modify_booking(booking: Booking, authorization: Annotated[str | None, Header()] = None) -> Booking:
    _user_id = utils.authorize(authorization)
    if _user_id != booking.user_id:
        raise HTTPException(status_code=401)
    booking = await booking.modify_booking() # raises ValidationError
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    else:
        return booking

@booking_router.delete(
    "/{booking_id}", status_code=status.HTTP_204_NO_CONTENT,
    responses = {
        400: { "description": "Bad request" },
        401: { "description": "Unauthorized" },
        404: { "description": "Booking not found" },
    }
)
async def delete_booking(booking_id: str, authorization: Annotated[str | None, Header()] = None) -> None:
    if not utils.is_safe_string(booking_id, 32):
        raise HTTPException(status_code=400, detail="Unsafe input")
    booking = await Booking.by_booking_id(booking_id)
    if booking is None:
        raise HTTPException(status_code=404)
    _user_id = utils.authorize(authorization)
    if _user_id != booking.user_id:
        raise HTTPException(status_code=401)
    await booking.cancel_booking()
    return

