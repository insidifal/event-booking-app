from app.models.account import Account
import app.utils as utils
from fastapi import APIRouter, Header, status, HTTPException
from typing import Annotated

account_router = APIRouter(prefix="/user/account", tags=["Account"])

@account_router.get(
    "",
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
    }
)
async def get_account(authorization: Annotated[str | None, Header()] = None) -> Account | None:
    user_id = utils.authorize(authorization) # raises HTTPException
    account = await Account.by_user_id(user_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        return account

@account_router.post(
    "", status_code=status.HTTP_201_CREATED,
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
    }
)
async def post_open_account(authorization: Annotated[str | None, Header()] = None) -> Account:
    user_id = utils.authorize(authorization) # raises HTTPException
    return await Account(user_id=user_id).open()

@account_router.put(
    "",
    responses = {
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
    }
)
async def post_update_balance(account: Account, authorization: Annotated[str | None, Header()] = None) -> Account:
    _user_id = utils.authorize(authorization)
    if _user_id != account.user_id:
        raise HTTPException(status_code=401)
    account = await account.update_balance() # raises ValidationError
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        return account

@account_router.delete(
    "/{account_id}", status_code=status.HTTP_204_NO_CONTENT,
    responses = {
        400: { "description": "Bad request" },
        401: { "description": "Unauthorized" },
        404: { "description": "User not found" },
    }
)
async def delete_account(account_id: str, authorization: Annotated[str | None, Header()] = None) -> None:
    if not utils.is_safe_string(account_id, 32):
        raise HTTPException(status_code=400, detail="Unsafe input")
    _user_id = utils.authorize(authorization)
    account = await Account.by_user_id(_user_id)
    if _user_id != account.user_id:
        raise HTTPException(status_code=401)
    await account.delete_account()
    return

