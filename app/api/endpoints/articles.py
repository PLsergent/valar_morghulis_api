from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Article])
def read_articles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items.
    """
    items = crud.article.get_multi_by_author(
        db=db, author_id=current_user.id, skip=skip, limit=limit
    )
    return items


@router.post("/new", response_model=schemas.Article)
def create_article(
    *,
    db: Session = Depends(deps.get_db),
    article_in: schemas.ArticleCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new article.
    """
    article = crud.article.create_with_author(
        db=db, obj_in=article_in, author_id=current_user.id
    )
    return article


@router.get("/{id}", response_model=schemas.Article)
def read_article(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get article by ID.
    """
    article = crud.article.get(db=db, id=id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.put("/{id}", response_model=schemas.Article)
def update_article(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    article_in: schemas.ArticleUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an article.
    """
    article = crud.article.get(db=db, id=id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article = crud.article.update(db=db, db_obj=article, obj_in=article_in)
    return article


@router.delete("/{id}", response_model=schemas.Article)
def delete_article(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an article.
    """
    article = crud.article.get(db=db, id=id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article = crud.article.remove(db=db, id=id)
    return article
