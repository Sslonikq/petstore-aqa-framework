import allure
import pytest

from api import UserApi
from models import ApiResponse, User

pytestmark = [allure.epic("User"), allure.feature("Сессия")]


@allure.title("Вход с верными учётными данными")
@pytest.mark.positive
def test_login_with_valid_credentials(user_api: UserApi, created_user: User) -> None:
    response = user_api.login(created_user.username, created_user.password)
    assert response.status_code == 200

    logged_in = ApiResponse.model_validate(response.json())
    assert logged_in.code == 200
    assert "logged in user session" in logged_in.message


@allure.title("Вход с неверным паролем всё равно успешен")
@pytest.mark.negative
def test_login_with_wrong_password_still_succeeds(user_api: UserApi, created_user: User) -> None:
    response = user_api.login(created_user.username, "definitely-wrong-password")

    # Расхождение с контрактом: swagger.json объявляет 400 "Invalid username/password supplied",
    # но сервер выдаёт сессию на любой пароль - аутентификации фактически нет.
    assert response.status_code == 200
    assert "logged in user session" in ApiResponse.model_validate(response.json()).message


@allure.title("Выход из сессии")
@pytest.mark.positive
def test_logout(user_api: UserApi) -> None:
    response = user_api.logout()
    assert response.status_code == 200

    logged_out = ApiResponse.model_validate(response.json())
    assert logged_out.code == 200
    assert logged_out.message == "ok"
