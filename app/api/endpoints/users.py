from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/register", response_model=schemas.User)
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


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me/update", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    username: str = Body(None),
    name: str = Body(None),
    firstname: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if name is not None:
        user_in.name = name
    if firstname is not None:
        user_in.firstname = firstname
    if email is not None:
        user_in.email = email
    if username is not None:
        user_in.username = username
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user
