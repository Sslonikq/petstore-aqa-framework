from faker import Faker

from models import User

faker = Faker()


class UserFactory:
    @staticmethod
    def build(**overrides) -> User:
        data = {
            "id": faker.random_int(min=100000, max=999999999),
            "username": faker.user_name(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "password": faker.password(),
            "phone": faker.phone_number(),
            "user_status": 1,
        }
        data.update(overrides)
        return User(**data)
