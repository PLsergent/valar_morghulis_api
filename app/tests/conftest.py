from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.db import session
from app.db.models import User
from app.main import app
from app.schemas import UserCreate
from app.tests.utils import get_token_headers


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def db() -> Generator:
    connection = session.engine.connect()
    transaction = connection.begin()
    test_session = Session(bind=connection, autocommit=False, autoflush=False)

    app.dependency_overrides[get_db] = lambda: test_session

    yield test_session

    app.dependency_overrides.pop(get_db)

    test_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user_data() -> Dict[str, str]:
    return {
        "email": "test@email.com",
        "username": "AniCepasSword14",
        "password": "nice_username_du_74",
        "public_key": "my_public_key",
    }


@pytest.fixture
def user(db: Session, user_data: Dict[str, str]) -> User:
    return crud.user.create(db, obj_in=UserCreate(**user_data))


@pytest.fixture
def auth_headers(client: TestClient, user: User, user_data: Dict[str, str]) -> None:
    return get_token_headers(
        client, username=user_data["username"], password=user_data["password"]
    )
