from pydantic import EmailStr, Field, field_validator

from src.models import CustomModel


class AnimeResponse(CustomModel):
    anime_id: int
    title: str
    synopsis: str
    episodes: int
    air_start_date: str
    air_end_date: str
    mal_score: float | None
    mal_ranked: int | None
    mal_popularity: int | None
    mal_members: int | None
