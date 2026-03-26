import app.model as model
from typing import Annotated
from fastapi import APIRouter, Header, HTTPException

main_router = APIRouter()
test_router = APIRouter(prefix="/tests", tags=["Tests"])

@main_router.get(
    "/user/login",
    responses = {
        400: { "description": "Invalid auth token" },
        401: { "description": "Unauthorized" },
        500: { "description": "Internal server error" },
    }
)
async def get_user_with_token(x_token: Annotated[str | None, Header()] = None):
    # Header will convert the parameter names characters from underscore (_)
    # to hyphen (-) to extract and document the headers.
    if not isinstance(x_token, str):
        raise HTTPException(status_code=400, detail="Invalid auth token")
    try:
        return await model.User.login(x_token)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500)
