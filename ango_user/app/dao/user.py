import sqlalchemy.exc
from pydantic import EmailStr

from ango_user.app.core.config import Settings
from ango_user.app.core.exceptions import DuplicateRecordException
from ango_user.app.db.connection import DbConnector
from ango_user.app.models.user import UserCreate, UserDb
from ango_user.app.schemas.user import User as UserOrm


settings = Settings()

db_connector = DbConnector(settings.DATABASE_URI)


def create(user_data: UserCreate) -> UserDb:
    session = db_connector.get_session()
    new_user_db = UserOrm(**user_data.dict())

    try:
        session.add(new_user_db)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise DuplicateRecordException(message="Account already exists.")

    return UserDb.from_orm(new_user_db)


def get_user_by_email(email: str) -> UserOrm | None:
    session = db_connector.get_session()
    users = list(session.query(UserOrm).filter(UserOrm.email == email))
    return users[0] if users else None


def delete(email: EmailStr):
    session = db_connector.get_session()
    session.query(UserOrm).filter(UserOrm.email == email).delete()
    session.commit()