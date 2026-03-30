import os
import re
import jwt
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

SECRET = "e58335f4169541f781130a68fe47bee6"

def is_safe_string(string: str, max_length: int = 20) -> bool:
    if string == None:
        return True
    if len(string) > max_length:
        return False
    safe_pattern = r"^[A-Za-z0-9 _!@#$&*.-]+$"
    check = re.fullmatch(safe_pattern, string)
    return check is not None

def create_token(user_id: str, expire_time: int = 3600) -> str:
    """
    Return JWT token for a user_id.
    """
    created = datetime.now(timezone.utc)
    expiry = datetime.now(timezone.utc) + timedelta(seconds=expire_time)
    payload = {
        "user_id": user_id,
        "iat": created,
        "exp": expiry
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def authorize(bearer: str) -> str:
    """
    Extract the bearer token and authorize.

    Returns the user_id or raises an HTTPException.
    """
    if bearer is None:
        raise HTTPException(status_code=401)
    token = bearer.removeprefix("Bearer ")

    if token is None:
        raise HTTPException(status_code=401)

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

