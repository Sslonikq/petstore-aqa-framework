import pytest
from pydantic.alias_generators import to_camel

from models import Order, Pet, PetstoreModel, User


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