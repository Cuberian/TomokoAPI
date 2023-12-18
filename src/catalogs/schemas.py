from typing import List

from pydantic import EmailStr, Field, field_validator

from src.animes.schemas import AnimeResponse
from src.models import CustomModel


class CatalogData(CustomModel):
    catalog_id: int
    name: str
    is_preview: bool = Field(False)
    description: str | None = Field(None)
    titles: List[AnimeResponse] | None = Field(None)