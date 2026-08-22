import httpx

from api.base_client import BaseApiClient
from models import Order


class StoreApi:
    def __init__(self, client: BaseApiClient) -> None:
        self._client = client

    def get_inventory(self) -> httpx.Response:
        return self._client.get("/store/inventory")

    def place_order(self, order: Order) -> httpx.Response:
        return self._client.post("/store/order", json=order.to_payload())

    def get_order(self, order_id: int) -> httpx.Response:
        return self._client.get(f"/store/order/{order_id}")

    def delete_order(self, order_id: int) -> httpx.Response:
        return self._client.delete(f"/store/order/{order_id}")
