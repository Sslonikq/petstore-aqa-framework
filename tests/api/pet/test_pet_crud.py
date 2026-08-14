import pytest

from api import PetApi
from models import Pet, PetStatus


@pytest.mark.smoke
@pytest.mark.positive
def test_create_pet(pet_api: PetApi) -> None:
    pet = Pet(
        id=987700001,
        name="rex",
        photo_urls=["http://example.com/1.jpg"],
        status=PetStatus.AVAILABLE,
    )

    response = pet_api.create_pet(pet)

    assert response.status_code == 200
    created = Pet.model_validate(response.json())
    assert created.id == pet.id
    assert created.name == pet.name


@pytest.mark.positive
def test_get_pet(pet_api: PetApi) -> None:
    pet = Pet(
        id=987700002,
        name="rex",
        photo_urls=["http://example.com/1.jpg"],
        status=PetStatus.AVAILABLE,
    )
    pet_api.create_pet(pet)

    response = pet_api.get_pet(pet.id)

    assert response.status_code == 200
    received = Pet.model_validate(response.json())
    assert received.id == pet.id
    assert received.name == pet.name


@pytest.mark.negative
def test_get_pet_returns_404_for_unknown_id(pet_api: PetApi) -> None:
    response = pet_api.get_pet(99999999)

    assert response.status_code == 404
