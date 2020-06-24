from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from app.db.base_class import Base


class User(Base):
    id = Column(
        UUID, primary_key=True, index=True, server_default=text('uuid_generate_v4()')
    )
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
