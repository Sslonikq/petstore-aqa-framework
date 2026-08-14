from collections.abc import Iterator

import pytest

from api import BaseApiClient, PetApi


@pytest.fixture(scope="session")
def api_client() -> Iterator[BaseApiClient]:
    client = BaseApiClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def pet_api(api_client: BaseApiClient) -> PetApi:
    return PetApi(api_client)
