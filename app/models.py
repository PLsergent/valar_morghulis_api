from sqlalchemy import Column, String, text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class User(Base):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=text("gen_random_uuid()"),
    )
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    public_key = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    reputation = Column(Boolean, nullable=False, default=0)


class Article(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=text('gen_random_uuid()')
    )
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    upvote = Column(Integer, nullable=False, default=0)
    downvote = Column(Integer, nullable=False, default=0)
    published = Column(Boolean, nullable=False, default=False)
    original = Column(Boolean, nullable=False, default=True)
    verified = Column(Boolean, nullable=False, default=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    author = relationship("User", foreign_keys=[author_id], backref="articles")
    readable_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    readable_by = relationship("User", foreign_keys=[readable_by_id], backref="readable_articles")
    files = relationship("File", backref="article")
    original_id = Column(UUID(as_uuid=True), ForeignKey('article.id'), nullable=True)
    original_article = relationship("Article", remote_side=[id])


class File(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=text('gen_random_uuid()')
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    path = Column(String, nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey('article.id'))