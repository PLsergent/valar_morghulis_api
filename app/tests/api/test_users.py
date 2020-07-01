from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.security import get_password_hash
from app.tests.utils import get_token_headers


@pytest.fixture
def user_data() -> Dict[str, str]:
    return {
        "email": "test@email.com",
        "username": "AniCepasSword14",
        "password": "nice_username_du_74",
        "public_key": "my_public_key",
    }


def test_create_user_new_email(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    r = client.post("/api/v1/users", json=user_data)
    assert r.status_code == 200

    created_user = r.json()
    user = crud.user.get_by_username(db, username=user_data["username"])
    assert user
    assert user.email == created_user["email"]
    assert user.username == created_user["username"]
    assert user.hashed_password[:6] == get_password_hash(user_data["password"])[:6]


def test_create_user_existing_email(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    user_in = UserCreate(
        email=user_data["email"],
        password="SoMeOthErPaSSWord",
        username="other_username",
        public_key="other_public_key",
    )
    crud.user.create(db, obj_in=user_in)

    r = client.post("/api/v1/users", json=user_data)
    assert r.status_code == 400
    assert r.json() == {"detail": "Email already taken."}


def test_create_user_existing_username(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    user_in = UserCreate(
        email="other@email.com",
        password="SoMeOthErPaSSWord",
        username=user_data["username"],
        public_key="other_public_key",
    )
    crud.user.create(db, obj_in=user_in)

    r = client.post("/api/v1/users", json=user_data)
    assert r.status_code == 400
    assert r.json() == {"detail": "Username already taken."}


def test_update_user_lastname(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    firstname = "Jean"
    lastname = "Dupont"
    user_in = UserCreate(**user_data, firstname=firstname, lastname=lastname)
    user = crud.user.create(db, obj_in=user_in)
    headers = get_token_headers(client, user_data["username"], user_data["password"])

    new_lastname = "Lewis"
    r = client.patch(
        "api/v1/users/me", json={"lastname": new_lastname}, headers=headers
    )
    assert r.status_code == 200
    assert user.lastname == new_lastname
    assert user.firstname == firstname
