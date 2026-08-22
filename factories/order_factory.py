from datetime import datetime, timedelta, timezone

from faker import Faker

from models import Order, OrderStatus

faker = Faker()


class OrderFactory:
    @staticmethod
    def build(**overrides) -> Order:
        data = {
            "id": faker.random_int(min=100000, max=999999999),
            "pet_id": faker.random_int(min=100000, max=999999999),
            "quantity": faker.random_int(min=1, max=10),
            "ship_date": (datetime.now(timezone.utc) + timedelta(days=7)).replace(microsecond=0),
            "status": OrderStatus.PLACED,
            "complete": False,
        }
        data.update(overrides)
        return Order(**data)
