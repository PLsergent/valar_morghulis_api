from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.db.models import Article, User
from app.schemas import ArticleCreate


@pytest.fixture
def article_data() -> Dict[str, str]:
    return {
        "title": "My article",
        "body": "my article's body",
    }


@pytest.fixture
def article(db: Session, article_data: Dict[str, str], user: User) -> Article:
    return crud.article.create_with_author(
        db, obj_in=ArticleCreate(**article_data), author_id=user.id
    )


def test_create_article(
    client: TestClient,
    db: Session,
    auth_headers: Dict[str, str],
    article_data: Dict[str, str],
) -> None:
    r = client.post("/articles", json=article_data, headers=auth_headers)
    assert r.status_code == 200

    created_article = r.json()
    article = crud.article.get(db, created_article["id"])
    assert created_article["title"] == article.title == article_data["title"]
    assert created_article["body"] == article.body == article_data["body"]


def test_remove_article(
    client: TestClient,
    db: Session,
    user: User,
    auth_headers: Dict[str, str],
    article: Article,
) -> None:
    r = client.delete(f"/articles/{article.id}", headers=auth_headers)
    assert r.status_code == 200
    assert crud.article.get(db, article.id) is None


def test_article_article(
    client: TestClient,
    db: Session,
    user: User,
    auth_headers: Dict[str, str],
    article: Article,
) -> None:
    new_title = "My New Title"
    r = client.patch(
        f"/articles/{article.id}", json={"title": new_title}, headers=auth_headers
    )
    assert r.status_code == 200
    assert article.title == r.json()["title"] == new_title
    assert article.body == r.json()["body"]
