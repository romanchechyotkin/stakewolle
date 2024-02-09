from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import SQLAlchemyError

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import TokenData
from src.referral.schemas import (CreateReferralRequest,
                                  CreateReferralResponse, GetReferralRequest,
                                  GetReferralResponse)
from src.referral.service import create_referral_code
from src.referral.utils import generate_referral_code

router = APIRouter(prefix="/referrals", tags=["Referral"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateReferralResponse)
async def create(
    data: CreateReferralRequest,
    jwt_data: TokenData = Depends(parse_jwt_user_data),
):
    print(data.expire_time_min)
    print(jwt_data)

    referral_code = generate_referral_code()
    expiration_time = datetime.utcnow() + timedelta(minutes=30)

    created_code = await create_referral_code(user_id=jwt_data.user_id, code=referral_code, expiration=expiration_time)
    print(created_code)

    return CreateReferralResponse(code=created_code["code"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetReferralResponse)
async def login(data: GetReferralRequest):
    print(data.email)

    return GetReferralResponse(code="")