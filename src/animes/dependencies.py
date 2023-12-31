from typing import Any
from src.animes import service
from src.animes.schemas import ReviewData, AnimeData
from src.exceptions import NotFound
from deep_translator import GoogleTranslator


async def valid_anime_id(anime_id: int) -> dict[str, Any]:
    anime = await service.get_by_id(anime_id)

    if not anime:
        mal_anime = service.get_by_mal_id(anime_id)

        if not mal_anime:
            raise NotFound()

        translated = GoogleTranslator(source='auto', target='ru')
        anime = AnimeData(
            title=mal_anime["title"],
            mal_anime_id=mal_anime["mal_anime_id"],
            synopsis=translated.translate(mal_anime["synopsis"]).replace("[Написано MAL Rewrite]", ""),
            preview_image_url=mal_anime["preview_image_url"],
            episodes=mal_anime["episodes"],
            air_start_date=mal_anime["air_start_date"],
            air_end_date=mal_anime["air_end_date"],
            mal_score=mal_anime["mal_score"],
            mal_ranked=mal_anime["mal_ranked"],
            mal_popularity=mal_anime["mal_popularity"],
            mal_members=mal_anime["mal_members"],
        )

        anime = await service.create_anime(anime)

    if anime['preview_image_url'] is None:
        mal_anime = service.get_by_mal_id(anime_id)
        anime['preview_image_url'] = mal_anime["preview_image_url"]


    return anime
