from app.models.user import User
import app.utils as utils
from fastapi import APIRouter, Header, status, HTTPException
from typing import Annotated

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get(
    "/me",
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
        500: { "description": "Internal server error" },
    }
)
async def get_user(x_token: Annotated[str | None, Header()] = None) -> User:
    payload = utils.check_token(x_token) # raises HTTPException
    _user_id = payload["user_id"]
    if await User.user_id_exists(_user_id):
        try:
            return await User.by_user_id(_user_id)
        except:
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=401)

@user_router.post(
    "", status_code=status.HTTP_201_CREATED,
    responses = {
        409: { "description": "Username already exists" },
        500: { "description": "Internal server error" },
    }
)
async def post_add_user(user: User) -> User:
    # Pydantic validates the input body so username is safe
    if not await User.username_exists(user.username):
        try:
            return await user.add_user()
        except:
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=409)

@user_router.put(
    "",
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
        500: { "description": "Internal server error" },
    }
)
async def post_modify_user(user: User, x_token: Annotated[str | None, Header()] = None) -> User:
    payload = utils.check_token(x_token)
    _user_id = payload["user_id"]
    if await User.user_id_exists(_user_id):
        _user = await User.by_user_id(_user_id)
        if _user.user_id != user.user_id:
            raise HTTPException(status_code=401)
        try:
            return await user.modify_user()
        except:
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=401)

@user_router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
        500: { "description": "Internal server error" },
    }
)
async def delete_user(user_id: str, x_token: Annotated[str | None, Header()] = None) -> None:
    payload = utils.check_token(x_token)
    _user_id = payload["user_id"]
    if await User.user_id_exists(_user_id):
        _user = await User.by_user_id(_user_id)
        if _user.user_id != user_id:
            raise HTTPException(status_code=401)
        try:
            await _user.delete_user()
            return
        except:
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=401)

