from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate


def get_token_response(client: TestClient, username: str, password: str) -> int:
    login_data = {"username": username, "password": password}
    return client.post("/login/token", data=login_data)


def test_get_access_token(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    user_in = UserCreate(**user_data)
    crud.user.create(db, obj_in=user_in)

    r = get_token_response(client, user_data["username"], user_data["password"])
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_wrong_passwd_access_token(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    user_in = UserCreate(**user_data)
    user = crud.user.create(db, obj_in=user_in)

    r = get_token_response(client, user.username, "BIIIIPWrongPassword")
    assert r.status_code == 400
    assert r.json() == {"detail": "Incorrect username or password."}


def test_wrong_username_access_token(client: TestClient, db: Session) -> None:
    r = get_token_response(client, "XXX", "BIIIIPWrongPassword")

    assert r.status_code == 400
    assert r.json() == {"detail": "Incorrect username or password."}


def test_use_access_token(
    client: TestClient, db: Session, user_data: Dict[str, str]
) -> None:
    user_in = UserCreate(**user_data)
    crud.user.create(db, obj_in=user_in)

    r = get_token_response(client, user_data["username"], user_data["password"])
    access_token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    r = client.post("/login/test-token", headers=headers)

    assert r.status_code == 200
    assert "username" in r.json()


def test_wrong_access_token(client: TestClient, db: Session) -> None:
    r = get_token_response(client, "XXX", "BIIIIPWrongPassword")

    tokens = r.json()
    assert tokens == {"detail": "Incorrect username or password."}

    headers = {"Authorization": "Bearer 'somethingthatisnotatoken'"}

    r = client.post("/login/test-token", headers=headers)

    assert r.status_code == 403
    assert r.json() == {"detail": "Could not validate credentials."}
