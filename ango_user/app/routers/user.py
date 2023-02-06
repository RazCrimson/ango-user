from fastapi import APIRouter, Depends

import ango_user.app.services.user as user_service
from ango_user.app.core.config import Settings
from ango_user.app.core.exceptions import AuthException
from ango_user.app.middleware.auth import authorize_service, authorize_user, parse_token
from ango_user.app.models.auth import TokenData
from ango_user.app.models.user import User, UserCreateRequest, UserDb, UserDeleteRequest

user_router = APIRouter()
settings = Settings()


@user_router.get("/me")
def read_users_me(token_data: TokenData = Depends(parse_token)) -> User:
    user = user_service.get_user_by_email(token_data.email)
    if user is None:
        raise AuthException(message="Invalid user")
    return user


@user_router.post("/")
def register_user(create_request: UserCreateRequest) -> UserDb:
    result = user_service.create(create_request)
    return result


@user_router.get("/{user_email}", dependencies=[Depends(authorize_service)])
def get_user_by_email(user_email: str) -> UserDb:
    user = user_service.get_user_by_email(user_email)
    return user


@user_router.delete("/", dependencies=[Depends(authorize_user)])
def delete_user(request: UserDeleteRequest):
    user_service.delete(request)
    return "Deleted"
