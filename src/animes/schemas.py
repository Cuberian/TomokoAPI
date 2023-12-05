from pydantic import EmailStr, Field, field_validator

from src.models import CustomModel


class AnimeResponse(CustomModel):
    anime_id: str
    title: str
    synopsis: str
    episodes: str
    episodes: int
    air_start_date: str
    air_end_date: str
    mal_score: float
    mal_ranked: int
    mal_popularity: int
    mal_members: int
