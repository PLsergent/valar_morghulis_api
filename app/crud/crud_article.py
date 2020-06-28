from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: ArticleCreate, id: str
    ) -> Article:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_author(
        self, db: Session, *, id: str, skip: int = 0, limit: int = 100
    ) -> List[Article]:
        return (
            db.query(self.model)
            .filter(Article.author_id == id)
            .offset(skip)
            .limit(limit)
            .all()
        )


article = CRUDArticle(Article)
