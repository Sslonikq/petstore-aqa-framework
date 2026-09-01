import allure
import pytest

from api import UserApi
from factories import UserFactory
from models import ApiResponse, User

pytestmark = [
    allure.epic("Интеграция"),
    allure.feature("Жизненный цикл пользователя"),
    pytest.mark.slow,
]


@allure.title("Пользователь проходит цикл создание - вход - обновление - удаление")
def test_user_lifecycle(
    user_api: UserApi,
    user_factory: type[UserFactory],
    user_cleanup: list[str],
) -> None:
    user = user_factory.build()
    user_cleanup.append(user.username)

    with allure.step("Создание пользователя"):
        response = user_api.create_user(user)
        assert response.status_code == 200, f"Failed to create user: {response.text}"

    with allure.step("Вход с учётными данными пользователя"):
        response = user_api.login(user.username, user.password)
        assert response.status_code == 200
        assert "logged in user session" in ApiResponse.model_validate(response.json()).message

    with allure.step("Созданный пользователь читается по имени"):
        response = user_api.get_user(user.username)
        assert response.status_code == 200

        created = User.model_validate(response.json())
        assert created.username == user.username
        assert created.first_name == user.first_name
        assert created.email == user.email

    new_first_name = "Updated"
    new_email = "updated@example.com"

    with allure.step("Обновление имени и почты"):
        user.first_name = new_first_name
        user.email = new_email

        response = user_api.update_user(user.username, user)
        assert response.status_code == 200

    with allure.step("Изменения сохранились на сервере"):
        response = user_api.get_user(user.username)
        assert response.status_code == 200

        stored = User.model_validate(response.json())
        assert stored.first_name == new_first_name
        assert stored.email == new_email

    with allure.step("Выход из сессии"):
        response = user_api.logout()
        assert response.status_code == 200

        logged_out = ApiResponse.model_validate(response.json())
        assert logged_out.code == 200
        assert logged_out.message == "ok"

    with allure.step("Удаление пользователя"):
        response = user_api.delete_user(user.username)
        assert response.status_code == 200

    with allure.step("Удалённый пользователь возвращает 404"):
        assert user_api.get_user(user.username).status_code == 404
