from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from app.db.base_class import Base


class User(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=text('gen_random_uuid()')
    )
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
