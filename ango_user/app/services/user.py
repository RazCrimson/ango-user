from uuid import UUID

import ango_user.app.dao.user as user_dao
from ango_user.app.core.exceptions import AuthException
from ango_user.app.core.hash import hash_password, verify_password
from ango_user.app.models.user import User, UserCreate, UserCreateRequest, UserDb, UserDeleteRequest
from ango_user.app.schemas.user import User as UserOrm


def create(create_request: UserCreateRequest) -> UserDb:
    hashed_password = hash_password(create_request.password)
    new_user = UserCreate(**create_request.dict(), pass_hash=hashed_password)
    created_user = user_dao.create(new_user)
    return created_user


def get_user_by_email(email: str) -> UserDb | None:
    return user_dao.get_user_by_email(email)


def delete(delete_request: UserDeleteRequest):
    user = get_user_by_email(delete_request.email)
    if not verify_password(delete_request.password, user.pass_hash):
        raise AuthException(message="Invalid password")
    user_dao.delete(delete_request.email)
