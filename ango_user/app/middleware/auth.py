from jose import JWTError, jwt
from pydantic import ValidationError
from fastapi import Cookie

from ango_user.app.core.config import Settings
from ango_user.app.core.exceptions import AuthException
from ango_user.app.models.auth import TokenData
from ango_user.app.models.user import UserBase

settings = Settings()


def parse_token(access_token: str = Cookie(...)) -> TokenData:
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData.parse_obj(payload)
        return token_data

    except (JWTError, ValidationError):
        raise AuthException(message="Invalid token")


def authorize_user(request: UserBase, access_token: str = Cookie(...)) -> None:
    token_data = parse_token(access_token)
    if token_data.email != request.email:
        raise AuthException(message="Unauthorized user")


def authorize_service(shared_secret: str = Cookie(...)):
    if shared_secret != settings.SECRET_KEY:
        raise AuthException(message="Unauthorized service")
