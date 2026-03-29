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
async def get_user(authorization: Annotated[str | None, Header()] = None) -> User:
    user_id = utils.authorize(authorization) # raises HTTPException
    try:
        return await User.by_user_id(user_id)
    except:
        raise HTTPException(status_code=500)

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
async def post_modify_user(user: User, authorization: Annotated[str | None, Header()] = None) -> User:
    _user_id = utils.authorize(authorization)
    if _user_id != user.user_id:
        raise HTTPException(status_code=401)
    try:
        return await user.modify_user()
    except:
        raise HTTPException(status_code=500)

@user_router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
        500: { "description": "Internal server error" },
    }
)
async def delete_user(user_id: str, authorization: Annotated[str | None, Header()] = None) -> None:
    _user_id = utils.authorize(authorization)
    if _user_id != user_id:
        raise HTTPException(status_code=401)
    try:
        user = await User.by_user_id(user_id)
        await user.delete_user()
        return
    except:
        raise HTTPException(status_code=500)

