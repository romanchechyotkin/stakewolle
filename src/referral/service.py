import sys
from datetime import timedelta
from typing import Any

from sqlalchemy import insert, update, select

from src.auth.exceptions import InternalServerError
from src.database import SessionLocal, fetch_one, referral_codes, users, referral_codes
from src.referral.schemas import ReferralCode

sys.path.append("..")


async def create_referral_code(user_id: str, code: str, expiration: timedelta) -> dict[str, Any] | None:
    db = SessionLocal()

    try:
        with db.begin():
            insert_query = (
                insert(referral_codes)
                .values(
                    {
                        "code": code,
                        "expiration": expiration,
                    }
                )
                .returning(referral_codes)
            )

            created_referral_code = await fetch_one(insert_query)

            update_query = (
                update(users)
                .where(users.c.id == int(user_id))
                .values(referral=created_referral_code["code"])
                .returning(users)
            )

            await fetch_one(update_query)

            db.commit()

    except Exception as e:
        print(e)
        db.rollback()
        raise InternalServerError()
    finally:
        db.close()
    
    return created_referral_code

async def get_referral_code_by_email(email: str) -> dict[str, Any] | None:
    select_query = select(users).where(users.c.email == email)
    
    return await fetch_one(select_query)