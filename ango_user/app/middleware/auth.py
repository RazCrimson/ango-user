from jose import JWTError, jwt
from pydantic import ValidationError
from fastapi import Cookie

from ango_user.app.core.config import Settings
from ango_user.app.core.exceptions import AuthException
from ango_user.app.models.auth import TokenData

settings = Settings()


def authorize_user(user_email: str, access_token: str = Cookie(...)):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData.parse_obj(payload)
        if token_data.email != user_email:
            raise AuthException(message="Unauthorized user")

    except (JWTError, ValidationError):
        raise AuthException(message="Invalid token")


def authorize_service(shared_secret: str = Cookie(...)):
    if shared_secret != settings.SECRET_KEY:
        raise AuthException(message="Unauthorized service")
