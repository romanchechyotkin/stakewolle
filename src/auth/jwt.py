import datetime
from datetime import timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from src.auth.exceptions import AuthRequired
from src.auth.schemas import TokenData
from src.auth.service import get_user_by_email
from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


async def parse_jwt_user_data(
    token: str = Depends(oauth2_scheme),
) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None:
            raise AuthRequired()
        token_data = TokenData(user_id=user_id, email=email)
    except PyJWTError:
        raise AuthRequired
    
    return token_data
