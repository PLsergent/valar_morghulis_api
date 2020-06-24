from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.security import get_password_hash


def test_create_user_new_email(client: TestClient, db: Session) -> None:
    email = "test@email.com"
    password = "AniCepasSword14"
    username = "nice_username_du_74"
    data = {"email": email, "password": password, "username": username}
    r = client.post("/users/register/",  json=data)

    assert r.status_code == 200
    created_user = r.json()
    user = crud.user.get_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]
    assert user.username == created_user["username"]
    assert user.hashed_password == get_password_hash(password)


def test_create_user_existing_email(
    client: TestClient, db: Session
) -> None:
    email = "test@email.com"
    password = "AniCepasSword14"
    username = "nice_username_du_74"
    user_in = UserCreate(
        email=email, password="SoMeOthErPaSSWord", username="other_username"
    )
    crud.user.create(db, obj_in=user_in)

    data = {"email": username, "password": password, "username": username}
    r = client.post("/users/register/",  json=data)

    assert r.status_code == 400
    assert r.json() == {"Email already taken."}


def test_create_user_existing_username(
    client: TestClient, db: Session
) -> None:
    email = "test@email.com"
    password = "AniCepasSword14"
    username = "nice_username_du_74"
    user_in = UserCreate(
        email="other@email.com", password="SoMeOthErPaSSWord", username=username
    )
    crud.user.create(db, obj_in=user_in)

    data = {"email": username, "password": password, "username": username}
    r = client.post("/users/register/",  json=data)

    assert r.status_code == 400
    assert r.json() == {"Username already taken."}
