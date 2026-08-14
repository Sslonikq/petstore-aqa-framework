import httpx

from api.base_client import BaseApiClient
from models import Pet, PetStatus


class PetApi:
    def __init__(self, client: BaseApiClient) -> None:
        self._client = client

    def create_pet(self, pet: Pet) -> httpx.Response:
        return self._client.post("/pet", json=pet.to_payload())

    def get_pet(self, pet_id: int) -> httpx.Response:
        return self._client.get(f"/pet/{pet_id}")

    def update_pet(self, pet: Pet) -> httpx.Response:
        return self._client.put("/pet", json=pet.to_payload())

    def delete_pet(self, pet_id: int) -> httpx.Response:
        return self._client.delete(f"/pet/{pet_id}")

    def find_pets_by_status(self, status: PetStatus | str) -> httpx.Response:
        return self._client.get("/pet/findByStatus", params={"status": status})
