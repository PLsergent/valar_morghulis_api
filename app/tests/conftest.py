from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db import session
from app.main import app


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
