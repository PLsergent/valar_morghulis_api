from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from app.db.base_class import Base
from app.db.mixins import UUIDPKMixin


class User(Base, UUIDPKMixin):
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    public_key = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    reputation = Column(Integer, nullable=False, default=0)


class Article(Base, UUIDPKMixin):
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    upvote = Column(Integer, nullable=False, default=0)
    downvote = Column(Integer, nullable=False, default=0)
    published = Column(Boolean, nullable=False, default=False)
    original = Column(Boolean, nullable=False, default=True)
    verified = Column(Boolean, nullable=False, default=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    author = relationship("User", foreign_keys=[author_id], backref="written_articles")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    owner = relationship("User", foreign_keys=[owner_id], backref="owned_articles")
    files = relationship("File", backref="article")
    original_article_id = Column(
        UUID(as_uuid=True), ForeignKey("article.id"), nullable=True
    )
    original_article = relationship("Article", remote_side="Article.id")

    @validates("author_id")
    def fill_in_owner_id(
        self: Article, _: Any, author_id: Optional[str]
    ) -> Optional[str]:
        if not self.owner_id:
            self.owner_id = author_id
        return author_id


class File(Base, UUIDPKMixin):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    path = Column(String, nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey("article.id"))
