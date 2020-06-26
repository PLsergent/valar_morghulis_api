from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FileBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    path: Optional[str] = None


class FileCreate(FileBase):
    name: str
    path: str


class FileUpdate(FileBase):
    pass


class FileInDBBase(FileBase):
    id: UUID
    name: str
    article_id: UUID

    class Config:
        orm_mode = True


class File(FileInDBBase):
    pass


class FileInDB(FileInDBBase):
    pass
