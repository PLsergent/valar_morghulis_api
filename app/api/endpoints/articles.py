from typing import Any, List
from uuid import UUID, uuid1

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.config import settings
from app.db import models

router = APIRouter()


@router.get("", response_model=List[schemas.ArticleOut])
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
        db=db, author_id=current_user.id, skip=skip, limit=limit
    )
    return articles


@router.post("", response_model=schemas.ArticleOut)
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


@router.get("/{article_id}", response_model=schemas.ArticleOut)
def read_article(
    *,
    db: Session = Depends(deps.get_db),
    article_id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get article by ID.
    """
    article = crud.article.get_by_id_and_owner(
        db=db, id=article_id, owner_id=current_user.id
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.patch("/{article_id}", response_model=schemas.ArticleOut)
def update_article(
    *,
    db: Session = Depends(deps.get_db),
    article_id: UUID,
    article_in: schemas.ArticleUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an article.
    """
    article = crud.article.get_by_id_and_owner(
        db=db, id=article_id, owner_id=current_user.id
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article = crud.article.update(db=db, db_obj=article, obj_in=article_in)
    return article


@router.delete("/{article_id}", response_model=schemas.ArticleOut)
def delete_article(
    *,
    db: Session = Depends(deps.get_db),
    article_id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an article.
    """
    article = crud.article.get_by_id_and_owner(
        db=db, id=article_id, owner_id=current_user.id
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    crud.article.remove(db, db_obj=article)
    return article


# Files


@router.get("/{article_id}/files", response_model=List[schemas.FileOut])
def read_files_per_article(
    *,
    db: Session = Depends(deps.get_db),
    article_id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve files.
    """
    article = crud.article.get_by_id_and_owner(
        db, id=article_id, owner_id=current_user.id
    )
    return article.files


@router.post("/{article_id}/files", response_model=List[schemas.FileOut])
def create_files_per_article(
    files: List[UploadFile] = File(...),
    *,
    db: Session = Depends(deps.get_db),
    s3: Any = Depends(deps.get_s3_client),
    article_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new files.
    """
    response = []
    for file in files:
        file_name = file.filename
        key = f"{current_user.id}/{article_id}/{file_name}"
        s3.put_object(
            Body=file.file,
            Bucket=f"{settings.AWS_STORAGE_BUCKET_NAME}",
            Key=key,
            ACL="public-read",
            CacheControl="max-age=31556926",  # 1 year
        )
        file_in: Any = {"name": file_name, "path": key}
        file_created = crud.file.create_with_article(
            db=db, obj_in=file_in, article_id=article_id
        )
        response.append(file_created)
    return response


# Alternative routes


@router.post("/{article_id}/files/bytes", response_model=List[str])
def create_files_bytes_per_article(
    files: List[bytes] = File(...),
    *,
    db: Session = Depends(deps.get_db),
    s3: Any = Depends(deps.get_s3_client),
    article_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Upload files to the s3.
    """
    response = []
    for file in files:
        key = f"{current_user.id}/{article_id}/{uuid1()}"
        s3.put_object(
            Body=file,
            Bucket=f"{settings.AWS_STORAGE_BUCKET_NAME}",
            Key=key,
            ACL="public-read",
            CacheControl="max-age=31556926",  # 1 year
        )
        response.append(key)
    return response


@router.post("/{article_id}/files/obj", response_model=List[schemas.FileOut])
def create_files_obj_per_article(
    *,
    db: Session = Depends(deps.get_db),
    s3: Any = Depends(deps.get_s3_client),
    article_id: str,
    files_in: List[schemas.FileCreate],
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new files objects using path.
    """
    response = []
    for file_in in files_in:
        file = crud.file.create_with_article(
            db=db, obj_in=file_in, article_id=article_id
        )
        response.append(file)
    return response


@router.get("/{article_id}/files/{file_id}", response_model=schemas.FileOut)
def read_file(
    *,
    db: Session = Depends(deps.get_db),
    article_id: UUID,
    file_id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get file by ID.
    """
    file = crud.file.get(db=db, id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.put("/{article_id}/files/{file_id}", response_model=schemas.FileOut)
def update_file(
    *,
    db: Session = Depends(deps.get_db),
    article_id: UUID,
    file_id: UUID,
    file_in: schemas.FileUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a file.
    """
    file = crud.file.get(db=db, id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file = crud.file.update(db=db, db_obj=file, obj_in=file_in)
    return file


@router.delete("/{article_id}/files", response_model=List[schemas.FileOut])
def delete_files_per_article(
    *,
    db: Session = Depends(deps.get_db),
    s3: Any = Depends(deps.get_s3_client),
    ids: List[UUID],
    article_id: UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a file.
    """
    response = []
    for id in ids:
        file = crud.file.get(db=db, id=id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        file = crud.file.remove(db=db, db_obj=file)
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file.path)
        response.append(file)
    return response
