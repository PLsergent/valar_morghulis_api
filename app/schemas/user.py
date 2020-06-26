from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    name: Optional[str] = None
    firstname: Optional[str] = None
    public_key: Optional[str] = None
    verified: bool = False
    reputation: int = 0


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str
    public_key: str = "XXX"


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[UUID] = None
    public_key: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
