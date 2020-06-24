from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None