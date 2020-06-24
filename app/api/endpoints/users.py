from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any, List
from sqlalchemy.orm import Session

from app import crud, models, schemas, security

router = APIRouter()


@router.post("/register", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(security.get_db),
    user_in: schemas.user.UserCreate
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
