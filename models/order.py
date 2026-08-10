from datetime import datetime
from enum import StrEnum

from models.base import PetstoreModel


class OrderStatus(StrEnum):
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


class Order(PetstoreModel):
    id: int | None = None
    pet_id: int | None = None
    quantity: int | None = None
    ship_date: datetime | None = None
    status: OrderStatus | None = None
    complete: bool | None = None
