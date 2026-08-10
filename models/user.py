from models.base import PetstoreModel


class User(PetstoreModel):
    id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    user_status: int | None = None