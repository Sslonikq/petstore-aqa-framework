from collections.abc import Callable

import pytest
from jsonschema import validate

from api import PetApi, StoreApi, UserApi
from factories import UserFactory
from models import Order, Pet, User


@pytest.mark.contract
def test_pet_response_matches_contract(
    pet_api: PetApi,
    created_pet: Pet,
    schema_for: Callable[[str], dict],
) -> None:
    response = pet_api.get_pet(created_pet.id)
    
    assert response.status_code == 200
    validate(response.json(), schema_for("Pet"))
    
    
@pytest.mark.contract
def test_order_response_matches_contract(
    store_api: StoreApi,
    created_order: Order,
    schema_for: Callable[[str], dict],
) -> None:
    response = store_api.get_order(created_order.id)
    
    assert response.status_code == 200
    validate(response.json(), schema_for("Order")) 
    
    
@pytest.mark.contract
def test_user_response_matches_contract(
    user_api: UserApi,
    created_user: User,
    schema_for: Callable[[str], dict],
) -> None:
    response = user_api.get_user(created_user.username)
    
    assert response.status_code == 200
    validate(response.json(), schema_for("User"))



@pytest.mark.contract
def test_create_user_response_matches_contract(
    user_api: UserApi,
    user_factory: type[UserFactory],
    user_cleanup: list[str],
    schema_for: Callable[[str], dict],
) -> None:
    user = user_factory.build()
    user_cleanup.append(user.username)
    response = user_api.create_user(user)
    
    assert response.status_code == 200
    validate(response.json(), schema_for("ApiResponse"))