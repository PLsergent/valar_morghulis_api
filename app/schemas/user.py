from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    public_key: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserOut(UserBase):
    id: UUID
    public_key: str

    class Config:
        orm_mode = True
