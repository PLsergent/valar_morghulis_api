from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.Article])
def read_articles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve articles.
    """
    articles = crud.article.get_multi_by_author(
        db=db, id=current_user.id, skip=skip, limit=limit
    )
    return articles


@router.post("/", response_model=schemas.Article)
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
        db=db, obj_in=article_in, id=current_user.id
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


# Files


@router.get("/{id}/files", response_model=List[schemas.File])
def read_files_per_article(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve files.
    """
    files = crud.file.get_multi_by_article(db=db, id=id, skip=skip, limit=limit)
    return files


@router.post("/{id}/files/", response_model=schemas.File)
def create_files(
    files: List[UploadFile] = File(...),
    *,
    db: Session = Depends(deps.get_db),
    s3: Any = Depends(deps.get_s3_client),
    id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new files.
    """
    for file in files:
        file_name = file.filename
        key = f"{current_user.id}/{id}/{file_name}"
        s3.put_object(
            Body=file.file,
            Bucket=f"{settings.AWS_STORAGE_BUCKET_NAME}",
            Key=key,
            ACL="public-read",
            CacheControl="max-age=31556926",  # 1 year
        )
        file_in: schemas.FileCreate = {"name": file_name, "path": key}
        file = crud.file.create_with_article(db=db, obj_in=file_in, id=id)
    return file


@router.get("/{article_id}/files/{id}", response_model=schemas.File)
def read_file(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get file by ID.
    """
    file = crud.file.get(db=db, id=id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.put("/{article_did}/files/{id}", response_model=schemas.File)
def update_file(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    file_in: schemas.FileUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a file.
    """
    file = crud.file.get(db=db, id=id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file = crud.file.update(db=db, db_obj=file, obj_in=file_in)
    return file


@router.delete("/{article_id}/files/{id}", response_model=schemas.File)
def delete_file(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a file.
    """
    file = crud.file.get(db=db, id=id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file = crud.file.remove(db=db, id=id)
    return file
