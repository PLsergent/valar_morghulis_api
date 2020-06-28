from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: UUID


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
