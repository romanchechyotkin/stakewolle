from datetime import timedelta

from pydantic import BaseModel, EmailStr


class CreateReferralRequest(BaseModel):
    expire_time_min: int

class CreateReferralResponse(BaseModel):
    code: str    

class GetReferralRequest(BaseModel):
    email: EmailStr

class GetReferralResponse(BaseModel):
    code: str

class GetShareURL(BaseModel):
    url: str

class ReferralCode(BaseModel):
    code: str
    expiration: timedelta