from app.models.user import User
import app.utils as utils
from fastapi import APIRouter, Header, HTTPException

main_router = APIRouter()
test_router = APIRouter(prefix="/tests", tags=["Tests"])

@main_router.get(
    "/user",
    responses = {
        400: { "description": "Bad username" },
        404: { "description": "User not found" },
        500: { "description": "Internal server error" },
    }
)
async def get_by_username(username: str) -> User:
    if utils.is_safe_string(username) and len(username) <= 15:
        if await User.username_exists(username):
            try:
                return await User.by_username(username)
            except:
                raise HTTPException(status_code=500)
        else:
            raise HTTPException(status_code=404)
    else:
        raise HTTPException(status_code=400)

@main_router.post(
    "/user",
    responses = {
        400: { "description": "Bad username" },
        500: { "description": "Internal server error" },
    }
)
async def post_new_user(user: User):
    # Pydantic validates the input body
    _username = user.username # username is safe at this point
    try:
        await User.new(_username)
    except:
        raise HTTPException(status_code=500)
