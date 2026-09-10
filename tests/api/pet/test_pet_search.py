import allure
import pytest

from api import PetApi
from factories import PetFactory
from models import PetStatus

pytestmark = [allure.epic("Pet"), allure.feature("Поиск")]


@allure.title("Поиск по статусу {status} возвращает только этот статус")
@pytest.mark.positive
@pytest.mark.parametrize("status", list(PetStatus))
def test_find_pets_by_status_returns_only_that_status(
    pet_api: PetApi,
    pet_factory: type[PetFactory],
    pet_cleanup: list[int],
    status: PetStatus,
) -> None:
    pet = pet_factory.build(status=status)
    pet_cleanup.append(pet.id)
    assert pet_api.create_pet(pet).status_code == 200

    response = pet_api.find_pets_by_status(status)
    assert response.status_code == 200
    pets = response.json()

    assert pet.id in [found["id"] for found in pets], "созданный питомец не найден по своему статусу"
    assert all(found["status"] == status for found in pets)


@allure.title("Поиск по несуществующему статусу возвращает пустой список")
@pytest.mark.negative
def test_find_pets_by_status_returns_empty_for_unknown_status(pet_api: PetApi) -> None:
    response = pet_api.find_pets_by_status("bogus")

    # Расхождение с контрактом: swagger.json объявляет ответ 400 "Invalid status value",
    # но сервер отвечает 200 с пустым списком на любое значение вне enum.
    assert response.status_code == 200
    assert response.json() == []
