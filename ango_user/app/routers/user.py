from fastapi import APIRouter, Cookie
from jose import JWTError, jwt
from pydantic import ValidationError

import ango_user.app.services.user as user_service
from ango_user.app.core.config import Settings
from ango_user.app.core.exceptions import AuthException
from ango_user.app.models.auth import TokenData
from ango_user.app.models.user import User, UserCreateRequest, UserDb, UserDeleteRequest

user_router = APIRouter()
settings = Settings()


@user_router.get("/me")
def read_users_me(access_token: str = Cookie(...)) -> User:
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData.parse_obj(payload)
    except (JWTError, ValidationError):
        raise AuthException(message="Invalid token detected")

    user = user_service.get_user_by_email(token_data.email)
    if user is None:
        raise AuthException(message="Invalid token detected")
    return user


@user_router.post("/")
def register_user(create_request: UserCreateRequest) -> UserDb:
    result = user_service.create(create_request)
    return result


@user_router.delete("/")
def delete_user(delete_request: UserDeleteRequest, access_token: str = Cookie(...)):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData.parse_obj(payload)
        if token_data.email != delete_request.email:
            raise AuthException(message="Invalid email detected")

    except (JWTError, ValidationError):
        raise AuthException(message="Invalid token detected")

    user_service.delete(delete_request)
    return "Deleted"
