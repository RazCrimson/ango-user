from uuid import UUID

from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    user_id: UUID
    email: EmailStr
