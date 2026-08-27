import allure
import pytest

from api import UserApi
from factories import UserFactory
from models import ApiResponse, User

pytestmark = [allure.epic("User"), allure.feature("CRUD")]


@allure.title("Создание пользователя")
@pytest.mark.smoke
@pytest.mark.positive
def test_create_user(
    user_api: UserApi,
    user_factory: type[UserFactory],
    user_cleanup: list[str],
) -> None:
    user = user_factory.build()
    user_cleanup.append(user.username)

    response = user_api.create_user(user)
    assert response.status_code == 200

    created = ApiResponse.model_validate(response.json())
    assert created.code == 200


@allure.title("Чтение созданного пользователя")
@pytest.mark.positive
def test_get_user(user_api: UserApi, created_user: User) -> None:
    response = user_api.get_user(created_user.username)
    assert response.status_code == 200

    received = User.model_validate(response.json())
    assert received.username == created_user.username
    assert received.first_name == created_user.first_name
    assert received.last_name == created_user.last_name
    assert received.email == created_user.email
    # Наблюдение: API возвращает пароль в открытом виде, вообще это дыра в реальном.
    assert received.password == created_user.password
    assert received.phone == created_user.phone


@allure.title("Обновление пользователя")
@pytest.mark.positive
def test_update_user(user_api: UserApi, created_user: User) -> None:
    new_first_name = "Updated"
    new_email = "updated@example.com"

    created_user.first_name = new_first_name
    created_user.email = new_email

    response = user_api.update_user(created_user.username, created_user)
    assert response.status_code == 200

    updated = ApiResponse.model_validate(response.json())
    assert updated.code == 200

    stored = User.model_validate(user_api.get_user(created_user.username).json())
    assert stored.first_name == new_first_name
    assert stored.email == new_email


@allure.title("Удаление пользователя")
@pytest.mark.positive
def test_delete_user(user_api: UserApi, created_user: User) -> None:
    response = user_api.delete_user(created_user.username)

    assert response.status_code == 200
    assert user_api.get_user(created_user.username).status_code == 404


@allure.title("Чтение несуществующего пользователя возвращает 404")
@pytest.mark.negative
def test_get_user_returns_404_for_unknown_username(user_api: UserApi) -> None:
    response = user_api.get_user("no_such_user_zzz_999")
    assert response.status_code == 404
