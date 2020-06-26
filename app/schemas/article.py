from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title
    body
    upvote
    downvote
    published
    original
    verified
    author_id
    readable_by_id
    original_id