from collections.abc import Callable

import pytest

from api import BaseApiClient


@pytest.fixture(scope="session")
def openapi_spec(api_client: BaseApiClient) -> dict:
    response = api_client.get("/swagger.json")
    assert response.status_code == 200, f"не удалось скачать спеку: {response.status_code}"
    return response.json()


@pytest.fixture(scope="session")
def schema_for(openapi_spec: dict) -> Callable[[str], dict]:
    def build(name: str) -> dict:
        return {"$ref": f"#/definitions/{name}", "definitions": openapi_spec["definitions"]}

    return build
