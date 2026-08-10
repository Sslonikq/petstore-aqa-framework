from models.base import PetstoreModel


class ApiResponse(PetstoreModel):
    code: int | None = None
    type: str | None = None
    message: str | None = None
