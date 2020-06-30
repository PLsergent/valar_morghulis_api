from typing import List
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.models import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: ArticleCreate, author_id: str
    ) -> Article:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_author(
        self, db: Session, *, author_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Article]:
        return (
            db.query(self.model)
            .filter_by(author_id=author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_and_owner(self, db: Session, *, id: UUID, owner_id: UUID) -> Article:
        return db.query(self.model).filter_by(id=id, owner_id=owner_id).one_or_none()


article = CRUDArticle(Article)
