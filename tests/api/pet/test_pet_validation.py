import pytest

from api import PetApi
from factories import PetFactory


@pytest.mark.negative
def test_create_pet_accepts_empty_name(
    pet_api: PetApi,
    pet_factory: type[PetFactory],
    pet_cleanup: list[int],
) -> None:
    pet = pet_factory.build(name="")
    pet_cleanup.append(pet.id)

    response = pet_api.create_pet(pet)
    assert response.status_code == 200

    # Контракту это не противоречит: required означает «поле передано»,
    # а не «значение непустое» - minLength в схеме Pet не объявлен.
    stored = pet_api.get_pet(pet.id)
    assert stored.json()["name"] == ""


@pytest.mark.negative
def test_create_pet_accepts_very_long_name(
    pet_api: PetApi,
    pet_factory: type[PetFactory],
    pet_cleanup: list[int],
) -> None:
    pet = pet_factory.build(name="a" * 10000)
    pet_cleanup.append(pet.id)

    response = pet_api.create_pet(pet)
    assert response.status_code == 200

    # maxLength в схеме Pet не объявлен, поэтому ограничения на длину нет.
    # Сравнение с исходным именем проверяет, что сервер не обрезал строку.
    stored = pet_api.get_pet(pet.id)
    assert stored.json()["name"] == pet.name