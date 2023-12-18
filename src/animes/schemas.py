import datetime

from pydantic import EmailStr, Field, field_validator

from src.models import CustomModel


class AnimeData(CustomModel):
    title: str
    synopsis: str
    episodes: int
    air_start_date: datetime.date
    air_end_date: datetime.date
    mal_score: float | None
    mal_ranked: int | None
    mal_popularity: int | None
    mal_members: int | None


class AnimeResponse(CustomModel):
    anime_id: int
    title: str
    synopsis: str
    episodes: int
    air_start_date: datetime.date
    air_end_date: datetime.date
    mal_score: float | None
    mal_ranked: int | None
    mal_popularity: int | None
    mal_members: int | None


class ReviewData(CustomModel):
    text: str | None
    overall_score: int = Field(int, ge=0, le=10)
    animation_score: int | None = Field(None, ge=0, le=10)
    sound_score: int | None = Field(None, ge=0, le=10)
    character_score: int | None = Field(None, ge=0, le=10)
    enjoyment_score: int | None = Field(None, ge=0, le=10)


class ReviewResponse(CustomModel):
    review_id: int
    anime_id: int
    text: str | None
    overall_score: int = Field(int, ge=0, le=10)
    animation_score: int | None = Field(None, ge=0, le=10)
    sound_score: int | None = Field(None, ge=0, le=10)
    character_score: int | None = Field(None, ge=0, le=10)
    enjoyment_score: int | None = Field(None, ge=0, le=10)
