from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any, List
from sqlalchemy.orm import Session

import security
import crud, models, schemas


router = APIRouter()


@router.post("/register/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(security.get_db),
    user_in: schemas.user.UserCreate,
    current_user: models.User = Depends(security.get_current_user),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user