from faker import Faker

from models import Pet, PetStatus

faker = Faker()


class PetFactory:
    @staticmethod
    def build(**overrides) -> Pet:
        data = {
            "id": faker.random_int(min=100000, max=999999999),
            "name": faker.name(),
            "photo_urls": [faker.image_url()],
            "status": PetStatus.AVAILABLE,
        }
        data.update(overrides)
        return Pet(**data)
