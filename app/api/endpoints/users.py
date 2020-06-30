from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.db import models

router = APIRouter()


@router.post("", response_model=schemas.UserOut)
def create_user(
    *, db: Session = Depends(deps.get_db), user_in: schemas.UserCreate
) -> Any:
    """
    Create new user.
    """
    user_based_on_username = crud.user.get_by_username(db, username=user_in.username)
    user_based_on_email = crud.user.get_by_email(db, email=user_in.email)

    if user_based_on_username:
        raise HTTPException(
            status_code=400, detail="Username already taken.",
        )

    if user_based_on_email:
        raise HTTPException(status_code=400, detail="Email already taken.")
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.UserOut)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.patch("/me", response_model=schemas.UserOut)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    user_in: schemas.UserUpdate
) -> Any:
    """
    Update own user.
    """
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user
