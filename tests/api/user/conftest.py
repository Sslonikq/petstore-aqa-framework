from collections.abc import Iterator

import pytest

from api import UserApi
from factories import UserFactory
from models import User


@pytest.fixture
def created_user(user_api: UserApi, user_factory: type[UserFactory]) -> Iterator[User]:
    user = user_factory.build()
    response = user_api.create_user(user)
    assert response.status_code == 200, f"Failed to create user: {response.text}"

    yield user

    user_api.delete_user(user.username)


@pytest.fixture
def user_cleanup(user_api: UserApi) -> Iterator[list[str]]:
    usernames: list[str] = []
    yield usernames

    for username in usernames:
        user_api.delete_user(username)
