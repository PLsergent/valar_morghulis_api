from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.models import File
from app.schemas.file import FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    def create_with_article(self, db: Session, *, obj_in: FileCreate, id: str) -> File:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, article_id=id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


file = CRUDFile(File)
