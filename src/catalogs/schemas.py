from typing import List

from pydantic import EmailStr, Field, field_validator

from src.animes.schemas import AnimeResponse
from src.models import CustomModel


class CatalogItems(CustomModel):
    items_ids: List[int]


class CatalogData(CustomModel):
    name: str
    is_preview: bool = Field(False)
    description: str | None = Field(None)


class CatalogResponse(CustomModel):
    catalog_id: int
    name: str
    is_preview: bool = Field(False)
    description: str | None = Field(None)
    titles: List[AnimeResponse] | None = Field(None)
