from datetime import datetime, timedelta
from typing import Any
import requests
from sqlalchemy import insert, select
from src.animes.config import anime_config
from src.database import  anime, fetch_one
from mal import Anime

async def get_top_5_animes() -> dict[str, Any] | None:
    select_query = select(anime)

    return await fetch_one(select_query)


async def get_by_id(anime_id: int) -> dict[str, Any] | None:
    select_query = select(anime).where(anime.c.anime_id == anime_id)
    return await fetch_one(select_query)


def get_by_mal_id(mal_anime_id: int) -> dict[str, Any] | None:
    # headers = {'Authorization': f'Bearer {anime_config.MAL_API_KEY}'}
    # r = requests.get(f'https://api.myanimelist.net/v2/anime/{mal_anime_id}', headers=headers)
    # return r.json()
    anime_obj = Anime(mal_anime_id)
    return {
        "anime_id": mal_anime_id,
        "title": anime_obj.title,
        "synopsis": anime_obj.synopsis,
        "episodes": anime_obj.episodes,
        "air_start_date": anime_obj.aired,
        "air_end_date": anime_obj.aired,
        "mal_score": anime_obj.score,
        "mal_ranked": anime_obj.rank,
        "mal_popularity": anime_obj.popularity,
        "mal_members": anime_obj.members,
        }
