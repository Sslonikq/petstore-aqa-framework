from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest

from api import AsyncApiClient, AsyncPetApi, BaseApiClient, PetApi, StoreApi, UserApi
from config import settings
from factories import OrderFactory, PetFactory, UserFactory


@pytest.fixture(scope="session", autouse=True)
def allure_environment(request: pytest.FixtureRequest) -> None:
    results_dir = request.config.getoption("--alluredir", default=None)
    if not results_dir:
        return

    lines = [
        f"BASE_URL={settings.base_url}",
        f"TIMEOUT={settings.timeout}",
        f"RETRY_COUNT={settings.retry_count}",
        f"API_KEY_SET={bool(settings.api_key)}",
    ]
    directory = Path(results_dir)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "environment.properties").write_text("\n".join(lines), encoding="utf-8")


@pytest.fixture(scope="session")
def api_client() -> Iterator[BaseApiClient]:
    client = BaseApiClient()
    yield client
    client.close()


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncApiClient]:
    client = AsyncApiClient()
    yield client
    await client.aclose()


@pytest.fixture(scope="session")
def pet_api(api_client: BaseApiClient) -> PetApi:
    return PetApi(api_client)


@pytest.fixture
def async_pet_api(async_client: AsyncApiClient) -> AsyncPetApi:
    return AsyncPetApi(async_client)


@pytest.fixture(scope="session")
def store_api(api_client: BaseApiClient) -> StoreApi:
    return StoreApi(api_client)


@pytest.fixture(scope="session")
def user_api(api_client: BaseApiClient) -> UserApi:
    return UserApi(api_client)


@pytest.fixture
def pet_factory() -> type[PetFactory]:
    return PetFactory


@pytest.fixture
def order_factory() -> type[OrderFactory]:
    return OrderFactory


@pytest.fixture
def user_factory() -> type[UserFactory]:
    return UserFactory


