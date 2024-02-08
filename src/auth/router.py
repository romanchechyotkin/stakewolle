from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from src.auth.exceptions import EmailNotFound, WrongPassword
from src.auth.jwt import create_access_token, create_refresh_token
from src.auth.schemas import AuthUser, LoginResponse, RegistrationResponse
from src.auth.security import check_password
from src.auth.service import create_user, get_user_by_email

# from src.auth import jwt, service, utils
# from src.auth.dependencies import (
#     valid_refresh_token,
#     valid_refresh_token_user,
#     valid_user_create,
# )
# from src.auth.jwt import parse_jwt_user_data
# from src.auth.schemas import AccessTokenResponse, AuthUser, JWTData, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=RegistrationResponse)
async def registration(user: AuthUser):
    print(user.email, user.password)

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


# @router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
# async def register_user(
#     auth_data: AuthUser = Depends(valid_user_create),
# ) -> dict[str, str]:
#     user = await service.create_user(auth_data)
#     return {
#         "email": user["email"],
#     }


# @router.get("/users/me", response_model=UserResponse)
# async def get_my_account(
#     jwt_data: JWTData = Depends(parse_jwt_user_data),
# ) -> dict[str, str]:
#     user = await service.get_user_by_id(jwt_data.user_id)

#     return {
#         "email": user["email"],
#     }


# @router.post("/users/tokens", response_model=AccessTokenResponse)
# async def auth_user(auth_data: AuthUser, response: Response) -> AccessTokenResponse:
#     user = await service.authenticate_user(auth_data)
#     refresh_token_value = await service.create_refresh_token(user_id=user["id"])

#     response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

#     return AccessTokenResponse(
#         access_token=jwt.create_access_token(user=user),
#         refresh_token=refresh_token_value,
#     )


# @router.put("/users/tokens", response_model=AccessTokenResponse)
# async def refresh_tokens(
#     worker: BackgroundTasks,
#     response: Response,
#     refresh_token: dict[str, Any] = Depends(valid_refresh_token),
#     user: dict[str, Any] = Depends(valid_refresh_token_user),
# ) -> AccessTokenResponse:
#     refresh_token_value = await service.create_refresh_token(
#         user_id=refresh_token["user_id"]
#     )
#     response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

#     worker.add_task(service.expire_refresh_token, refresh_token["uuid"])
#     return AccessTokenResponse(
#         access_token=jwt.create_access_token(user=user),
#         refresh_token=refresh_token_value,
#     )


# @router.delete("/users/tokens")
# async def logout_user(
#     response: Response,
#     refresh_token: dict[str, Any] = Depends(valid_refresh_token),
# ) -> None:
#     await service.expire_refresh_token(refresh_token["uuid"])

#     response.delete_cookie(
#         **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
#     )