from typing import List
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import File
from app.schemas.file import FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    def create_with_article(self, db: Session, *, obj_in: FileCreate, id: str) -> File:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, article_id=id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_article(
        self, db: Session, *, id: UUID, skip: int = 0, limit: int = 100
    ) -> List[File]:
        return (
            db.query(self.model)
            .filter(File.article_id == id)
            .offset(skip)
            .limit(limit)
            .all()
        )


file = CRUDFile(File)
