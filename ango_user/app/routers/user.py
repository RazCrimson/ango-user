from fastapi import APIRouter, Depends

import ango_user.app.services.user as user_service
from ango_user.app.core.config import Settings
from ango_user.app.core.exceptions import AuthException
from ango_user.app.middleware.auth import authorize_user, authorize_service
from ango_user.app.models.user import User, UserCreateRequest, UserDb, UserDeleteRequest

user_router = APIRouter()
settings = Settings()


@user_router.get("/me/{user_email}", dependencies=[Depends(authorize_user)])
def read_users_me(user_email: str) -> User:
    user = user_service.get_user_by_email(user_email)
    if user is None:
        raise AuthException(message="Invalid user")
    return user


@user_router.post("/")
def register_user(create_request: UserCreateRequest) -> UserDb:
    result = user_service.create(create_request)
    return result


@user_router.get("/{user_email}", dependencies=[Depends(authorize_service)])
def get_user_by_email(user_email: str) -> User:
    user = user_service.get_user_by_email(user_email)
    return user


@user_router.delete("/{user_email}", dependencies=[Depends(authorize_user)])
def delete_user(delete_request: UserDeleteRequest):
    user_service.delete(delete_request)
    return "Deleted"
