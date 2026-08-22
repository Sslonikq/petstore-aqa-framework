import pytest

from api import StoreApi
from factories import OrderFactory
from models import Order, PetStatus


@pytest.mark.smoke
@pytest.mark.positive
def test_place_order(
    store_api: StoreApi,
    order_factory: type[OrderFactory],
    order_cleanup: list[int],
) -> None:
    order = order_factory.build()
    order_cleanup.append(order.id)

    response = store_api.place_order(order)
    assert response.status_code == 200

    stored = Order.model_validate(store_api.get_order(order.id).json())
    assert stored == order


@pytest.mark.positive
def test_get_order(store_api: StoreApi, created_order: Order) -> None:
    response = store_api.get_order(created_order.id)

    assert response.status_code == 200
    received = Order.model_validate(response.json())
    assert received == created_order


@pytest.mark.positive
def test_delete_order(store_api: StoreApi, created_order: Order) -> None:
    response = store_api.delete_order(created_order.id)

    # Расхождение с контрактом: swagger.json объявляет у DELETE только 400 и 404,
    # успешный ответ не описан вовсе. Сервер отдаёт 200 с телом ApiResponse.
    assert response.status_code == 200

    assert store_api.get_order(created_order.id).status_code == 404


@pytest.mark.negative
def test_get_order_returns_404_for_unknown_id(store_api: StoreApi) -> None:
    response = store_api.get_order(99999999)

    assert response.status_code == 404


@pytest.mark.positive
def test_get_inventory(store_api: StoreApi) -> None:
    response = store_api.get_inventory()
    assert response.status_code == 200

    inventory = response.json()
    assert isinstance(inventory, dict)
    assert all(status in inventory for status in PetStatus)
    assert all(isinstance(count, int) for count in inventory.values())
