import asyncio

import allure
import pytest

from api import AsyncPetApi
from factories import PetFactory
from models import Pet

pytestmark = [
    allure.epic("Pet"),
    allure.feature("Конкурентность"),
    pytest.mark.concurrent,
    pytest.mark.positive,
    pytest.mark.slow,
]

CONCURRENT_REQUESTS = 10


@allure.title("Десять питомцев создаются параллельно")
async def test_create_pets_concurrently(
    async_pet_api: AsyncPetApi,
    pet_factory: type[PetFactory],
    pet_cleanup: list[int],
) -> None:
    pets = [pet_factory.build() for _ in range(CONCURRENT_REQUESTS)]
    pet_cleanup.extend(pet.id for pet in pets)

    responses = await asyncio.gather(*(async_pet_api.create_pet(pet) for pet in pets))

    assert all(response.status_code == 200 for response in responses)

    read_responses = await asyncio.gather(*(async_pet_api.get_pet(pet.id) for pet in pets))
    assert all(response.status_code == 200 for response in read_responses)

    stored_pets = [Pet.model_validate(response.json()) for response in read_responses]
    assert [pet.id for pet in stored_pets] == [pet.id for pet in pets]


@allure.title("Десять параллельных чтений возвращают одного и того же питомца")
async def test_read_same_pet_concurrently(
    async_pet_api: AsyncPetApi,
    created_pet: Pet,
) -> None:
    responses = await asyncio.gather(
        *(async_pet_api.get_pet(created_pet.id) for _ in range(CONCURRENT_REQUESTS))
    )
    assert all(response.status_code == 200 for response in responses)

    stored_pets = [Pet.model_validate(response.json()) for response in responses]
    assert all(pet == stored_pets[0] for pet in stored_pets)
