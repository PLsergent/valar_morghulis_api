from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .file import FileCreate, FileOut


class ArticleBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class ArticleCreate(ArticleBase):
    title: str
    body: str
    files: Optional[List[FileCreate]] = []


class ArticleUpdate(ArticleBase):
    pass


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
    files: Optional[List[FileOut]]

    class Config:
        orm_mode = True
