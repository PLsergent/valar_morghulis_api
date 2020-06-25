from typing import Any
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from app import crud
from app.schemas.user import UserCreate


def get_token(client: TestClient, username: str, password: str) -> Any:
    login_data = {
        "username": username,
        "password": password
    }
    return client.post("/login/token",  data=login_data)


def test_get_access_token(client: TestClient, db: Session) -> None:
    password = "PassWordCool"

    user_in = UserCreate(
        email="user@user.com", password=password, username="other_username"
    )
    user = crud.user.create(db, obj_in=user_in)

    r = get_token(client, user.username, password)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_wrong_passwd_access_token(client: TestClient, db: Session) -> None:
    password = "PassWordCool"

    user_in = UserCreate(
        email="user@user.com", password=password, username="other_username"
    )
    user = crud.user.create(db, obj_in=user_in)

    r = get_token(client, user.username, "BIIIIPWrongPassword")
    assert r.status_code == 400
    assert r.json() == {"detail": "Incorrect username or password."}


def test_wrong_username_access_token(client: TestClient, db: Session) -> None:
    r = get_token(client, "XXX", "BIIIIPWrongPassword")

    assert r.status_code == 400
    assert r.json() == {"detail": "Incorrect username or password."}


def test_use_access_token(
    client: TestClient, db: Session
) -> None:
    password = "PassWordCool"

    user_in = UserCreate(
        email="user@user.com", password=password, username="other_username"
    )
    user = crud.user.create(db, obj_in=user_in)

    response = get_token(client, user.username, password)
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.post("/login/test-token", headers=headers)

    assert r.status_code == 200
    assert "username" in r.json()


def test_wrong_access_token(
    client: TestClient, db: Session
) -> None:
    response = get_token(client, "XXX", "BIIIIPWrongPassword")

    tokens = response.json()
    assert tokens == {"detail": "Incorrect username or password."}

    headers = {"Authorization": f"Bearer 'somethingthatisnotatoken'"}

    r = client.post("/login/test-token", headers=headers)

    assert r.status_code == 403
    assert r.json() == {"detail": "Could not validate credentials."}
