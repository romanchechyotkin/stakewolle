from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from src.auth.exceptions import EmailNotFound, EmailTaken, WrongPassword
from src.auth.jwt import create_access_token, create_refresh_token
from src.auth.schemas import AuthUser, LoginResponse, RegistrationResponse
from src.auth.security import check_password
from src.auth.service import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=RegistrationResponse)
async def registration(user: AuthUser):
    print(user.email, user.password)

    user_data = await get_user_by_email(user.email)
    if user_data:
        raise EmailTaken()

    try:
        auth_data = await create_user(user)
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        error_msg = "Database execution error: {}".format(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg)

    print(auth_data)

    return RegistrationResponse(email=auth_data["email"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(user: AuthUser):
    print(user.email, user.password)

    try:
        user_data = await get_user_by_email(str(user.email))
        if not user_data:
            raise EmailNotFound()
        if not check_password(user.password, user_data["password"]):
            raise WrongPassword()
        
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        error_msg = "Database execution error: {}".format(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg)

    print(user_data)

    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )