from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    upvote: int = 0
    downvote: int = 0
    published: bool = False
    original: bool = True
    verified: bool = False


class ArticleCreate(ArticleBase):
    title: str
    body: str


class ArticleUpdate(ArticleBase):
    pass


class ArticleInDBBase(ArticleBase):
    id: UUID
    title: str
    author_id: UUID
    readable_by_id: Optional[UUID] = None
    original_id: Optional[UUID] = None

    class Config:
        orm_mode = True


class Article(ArticleInDBBase):
    pass


class ArticleInDB(ArticleInDBBase):
    pass
