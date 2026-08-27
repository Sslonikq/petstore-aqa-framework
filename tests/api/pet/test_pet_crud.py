import allure
import pytest

from api import PetApi
from factories import PetFactory
from models import Pet, PetStatus

pytestmark = [allure.epic("Pet"), allure.feature("CRUD")]


@allure.title("Создание питомца")
@pytest.mark.smoke
@pytest.mark.positive
def test_create_pet(
    pet_api: PetApi,
    pet_factory: type[PetFactory],
    pet_cleanup: list[int],
) -> None:
    pet = pet_factory.build()
    pet_cleanup.append(pet.id)

    response = pet_api.create_pet(pet)

    assert response.status_code == 200
    created = Pet.model_validate(response.json())
    assert created.id == pet.id
    assert created.name == pet.name


@allure.title("Чтение созданного питомца")
@pytest.mark.positive
def test_get_pet(pet_api: PetApi, created_pet: Pet) -> None:
    response = pet_api.get_pet(created_pet.id)

    assert response.status_code == 200
    received = Pet.model_validate(response.json())
    assert received.id == created_pet.id
    assert received.name == created_pet.name


@allure.title("Чтение несуществующего питомца возвращает 404")
@pytest.mark.negative
def test_get_pet_returns_404_for_unknown_id(pet_api: PetApi) -> None:
    response = pet_api.get_pet(99999999)

    assert response.status_code == 404


@allure.title("Обновление питомца сохраняется на сервере")
@pytest.mark.positive
def test_update_pet(pet_api: PetApi, created_pet: Pet) -> None:
    new_name = "Updated name"
    new_status = PetStatus.SOLD
    created_pet.name = new_name
    created_pet.status = new_status

    response = pet_api.update_pet(created_pet)

    assert response.status_code == 200
    received = Pet.model_validate(response.json())
    assert received.id == created_pet.id
    assert received.name == new_name
    assert received.status == new_status

    stored = Pet.model_validate(pet_api.get_pet(created_pet.id).json())
    assert stored.name == new_name
    assert stored.status == new_status


@allure.title("Удаление питомца")
@pytest.mark.positive
def test_delete_pet(pet_api: PetApi, created_pet: Pet) -> None:
    response = pet_api.delete_pet(created_pet.id)

    assert response.status_code == 200
    assert pet_api.get_pet(created_pet.id).status_code == 404
