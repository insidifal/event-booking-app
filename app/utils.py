import os
import re
import jwt
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

SECRET = "e58335f4169541f781130a68fe47bee6"

def is_safe_string(string: str) -> bool:
    if string == None:
        return True
    if len(string) > 20:
        return False
    safe_pattern = r"^[A-Za-z0-9_!@#$.-]+$"
    check = re.fullmatch(safe_pattern, string)
    return check is not None

def create_token(payload: dict, expire_time: int = 3600) -> str:
    created = datetime.now(timezone.utc)
    expiry = datetime.now(timezone.utc) + timedelta(seconds=expire_time)
    payload = payload | {"iat": created, "exp": expiry}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def check_token(token: str) -> dict | str:
    if token is None:
        raise HTTPException(status_code=401)
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

