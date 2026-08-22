from collections.abc import Iterator

import pytest

from api import PetApi
from factories import PetFactory
from models import Pet


@pytest.fixture
def created_pet(pet_api: PetApi, pet_factory: type[PetFactory]) -> Iterator[Pet]:
    pet = pet_factory.build()
    response = pet_api.create_pet(pet)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"

    yield pet

    pet_api.delete_pet(pet.id)


@pytest.fixture
def pet_cleanup(pet_api: PetApi) -> Iterator[list[int]]:
    ids: list[int] = []
    yield ids

    for pet_id in ids:
        pet_api.delete_pet(pet_id)