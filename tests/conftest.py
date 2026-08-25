from collections.abc import Iterator

import pytest

from api import PetApi, StoreApi, UserApi
from factories import OrderFactory, PetFactory, UserFactory
from models import Order, Pet, User


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


@pytest.fixture
def created_user(user_api: UserApi, user_factory: type[UserFactory]) -> Iterator[User]:
    user = user_factory.build()
    response = user_api.create_user(user)
    assert response.status_code == 200, f"Failed to create user: {response.text}"

    yield user

    user_api.delete_user(user.username)


@pytest.fixture
def user_cleanup(user_api: UserApi) -> Iterator[list[str]]:
    usernames: list[str] = []
    yield usernames

    for username in usernames:
        user_api.delete_user(username)
