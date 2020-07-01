from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FileBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class FileCreate(FileBase):
    name: str
    path: str


class FileUpdate(FileBase):
    pass


class FileOut(FileBase):
    id: UUID
    name: str
    path: str
    article_id: UUID

    class Config:
        orm_mode = True
