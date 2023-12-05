from typing import Any
from src.animes import service
from src.exceptions import NotFound


async def valid_anime_id(anime_id: int) -> dict[str, Any]:
    anime = await service.get_by_id(anime_id)

    if not anime:
        mal_anime = service.get_by_mal_id(anime_id)

        if not mal_anime:
            raise NotFound()

        anime = {
            "anime_id": anime_id,
            "title":  mal_anime["title"],
            "synopsis":  mal_anime["synopsis"],
            "episodes":  mal_anime["num_episodes"],
            "air_start_date":  mal_anime["start_date"],
            "air_end_date":  mal_anime["end_date"],
            "mal_score":  mal_anime["mean"],
            "mal_ranked":  mal_anime["rank"],
            "mal_popularity":  mal_anime["popularity"],
            "mal_members":  mal_anime["members"],
        }

    return anime
