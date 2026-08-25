from enum import StrEnum

import pytest
from pydantic.alias_generators import to_camel

from models import Order, OrderStatus, Pet, PetStatus, PetstoreModel, User


@pytest.mark.contract
@pytest.mark.parametrize(
    "model, schema_name",
    [(Pet, "Pet"), (Order, "Order"), (User, "User")],
)
def test_model_fields_match_contract(
    model: type[PetstoreModel],
    schema_name: str,
    openapi_spec: dict,
) -> None:
    our_fields = {to_camel(name) for name in model.model_fields}
    contract_fields = set(openapi_spec["definitions"][schema_name]["properties"])

    assert our_fields == contract_fields, (
        f"модель {schema_name} разошлась со спекой: "
        f"лишние у нас {our_fields - contract_fields}, "
        f"не описаны в модели {contract_fields - our_fields}"
    )


@pytest.mark.contract
@pytest.mark.parametrize(
    "model, schema_name",
    [(Pet, "Pet"), (Order, "Order"), (User, "User")],
)
def test_model_required_fields_match_contract(
    model: type[PetstoreModel],
    schema_name: str,
    openapi_spec: dict,
) -> None:
    our_required = {
        to_camel(name) for name, field in model.model_fields.items() if field.is_required()
    }
    contract_required = set(openapi_spec["definitions"][schema_name].get("required", []))

    assert our_required == contract_required, (
        f"модель {schema_name} разошлась со спекой: "
        f"обязательные только у нас {our_required - contract_required}, "
        f"обязательные только в спеке {contract_required - our_required}"
    )


@pytest.mark.contract
@pytest.mark.parametrize("enum_class, schema_name", [(PetStatus, "Pet"), (OrderStatus, "Order")])
def test_enum_values_match_contract(
    enum_class: type[StrEnum],
    schema_name: str,
    openapi_spec: dict,
) -> None:
    our_values = {status.value for status in enum_class}
    contract_values = set(openapi_spec["definitions"][schema_name]["properties"]["status"]["enum"])

    assert our_values == contract_values, (
        f"{enum_class.__name__} разошёлся со спекой: "
        f"только у нас {our_values - contract_values}, "
        f"только в спеке {contract_values - our_values}"
    )