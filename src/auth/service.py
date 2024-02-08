import sys
from typing import Any

from sqlalchemy import insert, select

from src.auth.schemas import AuthUser
from src.auth.security import hash_password
from src.database import fetch_one, users

sys.path.append("..")

async def create_user(user: AuthUser) -> dict[str, Any] | None:
    insert_query = (
        insert(users)
        .values(
            {
                "email": user.email,
                "password": hash_password(user.password),
            }
        )
        .returning(users)
    )

    return await fetch_one(insert_query)

async def get_user_by_email(email: str) -> dict[str, Any] | None:
    select_query = select(users).where(users.c.email == email)
    
    return await fetch_one(select_query)