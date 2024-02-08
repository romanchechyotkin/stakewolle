import datetime
from datetime import timedelta

import jwt

from src.config import settings


def create_access_token(user: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)

    jwt_data = {
        "sub": str(user["id"]),
        "email": str(user["email"]),
        "exp": expire,
    }
    
    encoded_data = jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    return encoded_data



def create_refresh_token(user: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(days=1)

    jwt_data = {
        "sub": str(user["id"]),
        "exp": expire,
    }

    encoded_data = jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    return encoded_data
