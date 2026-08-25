import pytest

from api import BaseApiClient, PetApi, StoreApi, UserApi
from models import Order, User


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="контракт объявляет 400 Invalid status value, "
    "сервер отвечает 200 с пустым списком на любое значение вне enum",
)
def test_find_by_status_rejects_invalid_value(pet_api: PetApi) -> None:
    response = pet_api.find_pets_by_status("invalid")

    assert response.status_code == 400


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="параметр status объявлен required, но без него сервер отвечает 200 с пустым списком",
)
def test_find_by_status_requires_status_param(api_client: BaseApiClient) -> None:
    # PetApi не даёт опустить обязательный параметр, поэтому идём через транспорт напрямую.
    response = api_client.get("/pet/findByStatus")

    assert response.status_code == 400


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="у orderId объявлен maximum: 10, но заказ с большим id читается с кодом 200",
)
def test_get_order_rejects_id_above_maximum(store_api: StoreApi, created_order: Order) -> None:
    # id из фабрики заведомо больше 10, значит по контракту запрос невалиден.
    response = store_api.get_order(created_order.id)

    assert response.status_code == 400


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="у DELETE объявлены только 400 и 404, "
    "но успешное удаление возвращает недокументированный 200",
)
def test_delete_order_response_is_documented(store_api: StoreApi, created_order: Order) -> None:
    response = store_api.delete_order(created_order.id)

    assert response.status_code in (400, 404)


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="контракт объявляет 400 Invalid username/password supplied, "
    "но сервер выдаёт сессию на любой пароль",
)
def test_login_rejects_wrong_password(user_api: UserApi, created_user: User) -> None:
    response = user_api.login(created_user.username, "definitely-wrong-password")

    assert response.status_code == 400