import allure
import pytest

from api import PetApi
from factories import PetFactory
from models import Pet, PetStatus

pytestmark = [
    allure.epic("Интеграция"),
    allure.feature("Жизненный цикл питомца"),
    pytest.mark.slow,
]


@allure.title("Питомец проходит цикл создание - чтение - обновление - удаление")
def test_pet_lifecycle(
    pet_api: PetApi,
    pet_factory: type[PetFactory],
    pet_cleanup: list[int],
) -> None:
    pet = pet_factory.build()
    pet_cleanup.append(pet.id)

    with allure.step("Создание питомца"):
        response = pet_api.create_pet(pet)
        assert response.status_code == 200

    with allure.step("Созданный питомец читается по id"):
        response = pet_api.get_pet(pet.id)
        assert response.status_code == 200

        created = Pet.model_validate(response.json())
        assert created.id == pet.id
        assert created.name == pet.name
        assert created.status == pet.status

    new_name = "Updated name"
    new_status = PetStatus.SOLD

    with allure.step("Обновление имени и статуса"):
        pet.name = new_name
        pet.status = new_status

        response = pet_api.update_pet(pet)
        assert response.status_code == 200

    with allure.step("Изменения сохранились на сервере"):
        response = pet_api.get_pet(pet.id)
        assert response.status_code == 200

        stored = Pet.model_validate(response.json())
        assert stored.id == pet.id
        assert stored.name == new_name
        assert stored.status == new_status

    with allure.step("Удаление питомца"):
        response = pet_api.delete_pet(pet.id)
        assert response.status_code == 200

    with allure.step("Удалённый питомец возвращает 404"):
        assert pet_api.get_pet(pet.id).status_code == 404
