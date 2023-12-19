from typing import Any, List
import requests
from sqlalchemy import insert, select
from src.animes.config import anime_config
from src.animes.schemas import ReviewData, AnimeData
from src.database import anime, fetch_one, fetch_all, review, execute
from mal import Anime
from src.animes.utils import convert_date
from deep_translator import GoogleTranslator


async def get_top_5_animes() -> List[dict[str, Any]] | None:
    top_5 = requests.get("https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=5",
                         headers={'Authorization': f'Bearer {anime_config.MAL_API_KEY}',
                                  'Origin': 'http://127.0.0.1:8000'})
    data = top_5.json()
    res = []
    for item in data['data']:
        anime_item = item['node']
        anime_res = requests.get(
            f"https://api.myanimelist.net/v2/anime/{anime_item['id']}?fields=id,title,main_picture,"
            f"alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,rating,"
            f"num_episodes,rating,pictures",
            headers={'Authorization': f'Bearer {anime_config.MAL_API_KEY}',
                     'Origin': 'http://127.0.0.1:8000'})
        anime_data = anime_res.json()

        anime_db_data = await get_by_id(anime_data['id'])
        if anime_db_data:
            res.append(anime_db_data)
            continue

        air_start_date = convert_date(anime_data['start_date']).date()
        air_end_date = convert_date(anime_data['end_date']).date()
        translated = GoogleTranslator(source='auto', target='ru')

        anime_data = AnimeData(
            mal_anime_id=anime_data['id'],
            title=anime_data['title'],
            synopsis=translated.translate(anime_data['synopsis']).replace("[Написано MAL Rewrite]", ""),
            episodes=anime_data['num_episodes'],
            air_start_date=air_start_date,
            air_end_date=air_end_date,
            mal_score=anime_data['mean'],
            mal_ranked=anime_data['rank'],
            mal_popularity=anime_data['popularity'],
            mal_members=None,
        )

        anime_data = await create_anime(anime_data)

        res.append(anime_data)
    return res


async def create_anime(anime_data: AnimeData) -> dict[str, Any] | None:
    exist_anime = await get_by_id(anime_data.mal_anime_id)
    if exist_anime is not None:
        return exist_anime

    insert_query = (
        insert(anime)
        .values(
            {
                "anime_id": anime_data.mal_anime_id,
                "title": anime_data.title,
                "synopsis": anime_data.synopsis,
                "episodes": anime_data.episodes,
                "air_start_date": anime_data.air_start_date,
                "air_end_date": anime_data.air_end_date,
                "mal_score": anime_data.mal_score,
                "mal_ranked": anime_data.mal_ranked,
                "mal_anime_id": anime_data.mal_anime_id,
                "mal_popularity": anime_data.mal_popularity,
                "mal_members": anime_data.mal_members,
            }
        )
        .returning(anime)
    )

    return await fetch_one(insert_query)


async def get_user_review(user_id: int, anime_id: int) -> dict[str, Any] | None:
    select_query = select(review).where(review.c.anime_id == anime_id and review.c.user_id == user_id)
    return await fetch_one(select_query)


async def get_user_reviews(user_id: int) -> List[dict[str, Any]] | None:
    select_query = select(review).where(review.c.user_id == user_id)
    return await fetch_all(select_query)


async def create_or_update_review(user_id: int, anime_id: int, review_data: ReviewData) -> dict[str, Any] | None:
    select_query = select(review).where(review.c.anime_id == anime_id and review.c.user_id == user_id)
    exist_review = await fetch_one(select_query)

    if exist_review is None:
        insert_query = (
            insert(review)
            .values(
                {
                    "anime_id": anime_id,
                    "user_id": user_id,
                    "text": review_data.text,
                    "overall_score": review_data.overall_score,
                    "animation_score": review_data.animation_score,
                    "sound_score": review_data.sound_score,
                    "character_score": review_data.character_score,
                    "enjoyment_score": review_data.enjoyment_score,
                }
            )
            .returning(review)
        )

        return await fetch_one(insert_query)

    update_query = (
        review.update()
        .values(
            {
                "text": review_data.text,
                "overall_score": review_data.overall_score,
                "animation_score": review_data.animation_score,
                "sound_score": review_data.sound_score,
                "character_score": review_data.character_score,
                "enjoyment_score": review_data.enjoyment_score,
            }
        ).where(review.c.review_id == exist_review['review_id'])
    )

    await execute(update_query)
    return exist_review


async def get_by_id(anime_id: int) -> dict[str, Any] | None:
    select_query = select(anime).where(anime.c.anime_id == anime_id)
    anime_item = await fetch_one(select_query)

    return anime_item


def get_by_mal_id(mal_anime_id: int) -> dict[str, Any] | None:
    anime_obj = Anime(mal_anime_id)

    if anime_obj is None:
        return None

    date_str1, date_str2 = anime_obj.aired.split(" to ") if " to " in anime_obj.aired \
        else [anime_obj.aired, anime_obj.aired]
    air_start_date = convert_date(date_str1).date()
    air_end_date = None if date_str2 == "?" else convert_date(date_str2).date()

    return {
        "anime_id": mal_anime_id,
        "mal_anime_id": mal_anime_id,
        "title": anime_obj.title,
        "synopsis": anime_obj.synopsis,
        "num_episodes": anime_obj.episodes,
        "air_start_date": air_start_date,
        "air_end_date": air_end_date,
        "mal_score": anime_obj.score,
        "mal_ranked": anime_obj.rank,
        "mal_popularity": anime_obj.popularity,
        "mal_members": anime_obj.members,
    }
