from typing import Dict

from fastapi.testclient import TestClient


def get_token_headers(
    client: TestClient, username: str, password: str
) -> Dict[str, str]:
    login_data = {"username": username, "password": password}
    r = client.post("/login/token", data=login_data)
    tokens = r.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
