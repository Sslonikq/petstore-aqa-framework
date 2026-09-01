import httpx

from api.async_client import AsyncApiClient
from models import Pet


class AsyncPetApi:
    def __init__(self, client: AsyncApiClient) -> None:
        self._client = client

    async def create_pet(self, pet: Pet) -> httpx.Response:
        return await self._client.post("/pet", json=pet.to_payload())

    async def get_pet(self, pet_id: int) -> httpx.Response:
        return await self._client.get(f"/pet/{pet_id}")
