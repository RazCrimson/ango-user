from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreateRequest(UserBase):
    init_vector: bytes
    password: bytes


class UserCreate(UserBase):
    init_vector: bytes
    pass_hash: bytes


class UserDbBase(UserBase):
    id: UUID
    init_vector: bytes
    last_signed_in: Optional[datetime] = None

    class Config:
        orm_mode = True


class User(UserDbBase):
    pass


class UserDb(UserDbBase):
    pass_hash: bytes


class UserDeleteRequest(UserBase):
    password: bytes
