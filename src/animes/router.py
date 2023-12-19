from datetime import datetime
from typing import Any, Mapping

from deep_translator import GoogleTranslator
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from src.animes.schemas import AnimeResponse, ReviewData, ReviewResponse, AnimeData
from src.animes import service, utils
from src.auth.exceptions import AuthRequired
from src.auth.schemas import JWTData
from src.auth.jwt import parse_jwt_user_data, parse_jwt_user_data_optional
from src.animes.dependencies import (
    valid_anime_id
)
from rec_sys.main import (
    get_recommendations
)
from src.auth import service as auth_service
from src.animes import service
from src.animes.utils import convert_date

router = APIRouter()


@router.get("/top", status_code=status.HTTP_200_OK, response_model=list[AnimeResponse])
async def get_top_5_animes():
    animes = await service.get_top_5_animes()
    res = []

    for item in animes:
        res.append(AnimeResponse(
            anime_id=item['anime_id'],
            mal_anime_id=item['mal_anime_id'],
            title=item['title'],
            synopsis=item['synopsis'],
            episodes=item['episodes'],
            air_start_date=item['air_start_date'],
            air_end_date=item['air_end_date'],
            mal_score=item['mal_score'],
            mal_ranked=item['mal_ranked'],
            mal_popularity=item['mal_popularity'],
            mal_members=None,
            review=None
        ))

    return res


@router.get("/anime/{anime_id}", status_code=status.HTTP_200_OK, response_model=AnimeResponse)
async def get_anime_by_id(jwt_data: JWTData = Depends(parse_jwt_user_data_optional),
                          anime: AnimeResponse = Depends(valid_anime_id)):
    review = None
    if jwt_data is not None:
        review = await service.get_user_review(jwt_data.user_id, anime['anime_id'])

    return {
        "anime_id": anime["anime_id"],
        "title":  anime["title"],
        "synopsis":  anime["synopsis"],
        "episodes":  anime["episodes"],
        "air_start_date":  anime["air_start_date"],
        "air_end_date":  anime["air_end_date"],
        "mal_score":  anime["mal_score"],
        "mal_ranked":  anime["mal_ranked"],
        "mal_popularity":  anime["mal_popularity"],
        "mal_members":  anime["mal_members"],
        "review": review
    }


# TODO
@router.get("/{anime_id}/screen-shots", status_code=status.HTTP_200_OK, response_model=AnimeResponse)
async def get_anime_screenshots_by_id(anime: AnimeResponse = Depends(valid_anime_id)):
    return {
        "anime_id": anime["anime_id"],
        "title":  anime["title"],
        "synopsis":  anime["synopsis"],
        "episodes":  anime["episodes"],
        "air_start_date":  anime["air_start_date"],
        "air_end_date":  anime["air_end_date"],
        "mal_score":  anime["mal_score"],
        "mal_ranked":  anime["mal_ranked"],
        "mal_popularity":  anime["mal_popularity"],
        "mal_members":  anime["mal_members"],
    }


@router.put("/{anime_id}/score", status_code=status.HTTP_200_OK, response_model=ReviewResponse)
async def put_anime_score_by_id(review_data: ReviewData,
                                anime: AnimeResponse = Depends(valid_anime_id),
                                jwt_data: JWTData = Depends(parse_jwt_user_data)):
    review = await service.create_or_update_review(jwt_data.user_id, anime['anime_id'], review_data)

    return {
        "anime_id": review["anime_id"],
        "review_id": review["review_id"],
        "text": review["text"],
        "overall_score": review["overall_score"],
        "animation_score": review["animation_score"],
        "sound_score": review["sound_score"],
        "character_score": review["character_score"],
        "enjoyment_score": review["enjoyment_score"],
    }


@router.get("/recommendations", status_code=status.HTTP_200_OK, response_model=list[AnimeResponse])
async def get_recs_for_user(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    reviews = await service.get_user_reviews(jwt_data.user_id)

    anime_ids = [item['anime_id'] for item in reviews]

    rec_animes = [service.get_by_mal_id(rec_uid) for rec_uid in get_recommendations(anime_ids)]
    translated = GoogleTranslator(source='auto', target='ru')
    res = []
    for anime in rec_animes:
        anime_data = AnimeData(
            title=anime["title"],
            mal_anime_id=anime["mal_anime_id"],
            synopsis=translated.translate(anime["synopsis"]).replace("[Написано MAL Rewrite]", ""),
            episodes=anime["episodes"],
            air_start_date=anime["air_start_date"],
            air_end_date=anime["air_end_date"],
            mal_score=anime["mal_score"],
            mal_ranked=anime["mal_ranked"],
            mal_popularity=anime["mal_popularity"],
            mal_members=anime["mal_members"],
        )

        anime_data = await service.create_anime(anime_data)
        res.append(anime_data)

    return rec_animes
