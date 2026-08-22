from collections.abc import Iterator

import pytest

from api import BaseApiClient, PetApi, StoreApi, UserApi
from factories import OrderFactory, PetFactory, UserFactory


@pytest.fixture(scope="session")
def api_client() -> Iterator[BaseApiClient]:
    client = BaseApiClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def pet_api(api_client: BaseApiClient) -> PetApi:
    return PetApi(api_client)


@pytest.fixture(scope="session")
def store_api(api_client: BaseApiClient) -> StoreApi:
    return StoreApi(api_client)



@pytest.fixture
def pet_factory() -> type[PetFactory]:
    return PetFactory


@pytest.fixture
def order_factory() -> type[OrderFactory]:
    return OrderFactory


@pytest.fixture(scope="session")
def user_api(api_client: BaseApiClient) -> UserApi:
    return UserApi(api_client)


@pytest.fixture
def user_factory() -> type[UserFactory]:
    return UserFactory