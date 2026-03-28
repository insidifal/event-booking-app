from app.models.user import User
import app.utils as utils
from fastapi import APIRouter, status, HTTPException

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post(
    "/login",
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
    }
)
async def login(user: User) -> dict:
    if await User.username_exists(user.username):
        _user = await User.by_username(user.username)
        if _user.verify_password(user.password):
            token = utils.create_token({"user_id": _user.user_id})
            return {"X-Token": token}
        else:
            raise HTTPException(status_code=401)
    else:
        raise HTTPException(status_code=404)

