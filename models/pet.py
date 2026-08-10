from enum import StrEnum

from models.base import PetstoreModel


class Category(PetstoreModel):
    id: int | None = None
    name: str | None = None


class Tag(PetstoreModel):
    id: int | None = None
    name: str | None = None


class PetStatus(StrEnum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class Pet(PetstoreModel):
    id: int | None = None
    category: Category | None = None
    name: str
    photo_urls: list[str]
    tags: list[Tag] | None = None
    status: PetStatus | None = None
