from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    init_vector: bytes


class UserCreateRequest(UserBase):
    password: bytes


class UserCreate(UserBase):
    pass_hash: bytes


class UserDbBase(UserBase):
    id: UUID
    last_signed_in: Optional[datetime] = None

    class Config:
        orm_mode = True


class User(UserDbBase):
    pass


class UserDb(UserDbBase):
    pass_hash: bytes


class UserDeleteRequest(BaseModel):
    email: EmailStr
    password: bytes
