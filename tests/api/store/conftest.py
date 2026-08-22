from collections.abc import Iterator

import pytest

from api import StoreApi
from factories import OrderFactory
from models import Order


@pytest.fixture
def created_order(store_api: StoreApi, order_factory: type[OrderFactory]) -> Iterator[Order]:
    order = order_factory.build()
    response = store_api.place_order(order)
    assert response.status_code == 200, f"Failed to create order: {response.text}"

    yield order

    store_api.delete_order(order.id)


@pytest.fixture
def order_cleanup(store_api: StoreApi) -> Iterator[list[int]]:
    ids: list[int] = []
    yield ids

    for order_id in ids:
        store_api.delete_order(order_id)
