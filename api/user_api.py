import httpx

from api.base_client import BaseApiClient
from models import User


class UserApi:
    def __init__(self, client: BaseApiClient) -> None:
        self._client = client

    def create_user(self, user: User) -> httpx.Response:
        return self._client.post("/user", json=user.to_payload())

    def get_user(self, username: str) -> httpx.Response:
        return self._client.get(f"/user/{username}")

    def update_user(self, username: str, user: User) -> httpx.Response:
        return self._client.put(f"/user/{username}", json=user.to_payload())

    def delete_user(self, username: str) -> httpx.Response:
        return self._client.delete(f"/user/{username}")

    def login(self, username: str, password: str) -> httpx.Response:
        return self._client.get(
            "/user/login",
            params={"username": username, "password": password},
        )

    def logout(self) -> httpx.Response:
        return self._client.get("/user/logout")
