from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class ArticleCreate(ArticleBase):
    title: str
    body: str


class ArticleUpdate(ArticleBase):
    title: str
    body: str
    published: Optional[bool] = False
    verified: Optional[bool] = False


class ArticleOut(ArticleBase):
    id: UUID
    author_id: UUID
    owner_id: UUID
    original_id: Optional[UUID] = None
    upvote: int
    downvote: int
    published: bool
    original: bool
    verified: bool

    class Config:
        orm_mode = True
