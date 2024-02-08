from src.exceptions import (BadRequest, NotAuthenticated, NotFound,
                            PermissionDenied)


class ErrorCode:
    AUTHENTICATION_REQUIRED = "Authentication required."
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    EMAIL_NOT_FOUND = "Email not found."
    WRONG_PASSWORD = "Incorrect password"
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN


class EmailNotFound(BadRequest):
    DETAIL = ErrorCode.EMAIL_NOT_FOUND


class WrongPassword(BadRequest):
    DETAIL = ErrorCode.WRONG_PASSWORD


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID