from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/register", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate
) -> Any:
    """
    Create new user.
    """
    user_based_on_username = crud.user.get_by_username(db, username=user_in.username)
    user_based_on_email = crud.user.get_by_email(db, email=user_in.email)

    if user_based_on_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken.",
        )
    
    if user_based_on_email:
        raise HTTPException(
            status_code=400,
            detail="Email already taken."
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
