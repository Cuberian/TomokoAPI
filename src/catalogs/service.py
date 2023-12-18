from typing import Any, List
from sqlalchemy import insert, select

from src.catalogs.schemas import CatalogData
from src.database import fetch_all, fetch_one, catalog, anime, catalog_anime


async def get_all_catalogs() -> List[dict[str, Any]] | None:
    select_query = select(catalog)
    return await fetch_all(select_query)


async def get_preview_catalogs() -> List[CatalogData] | None:
    select_query = select(catalog).where(catalog.c.is_preview is True)
    preview_catalogs = await fetch_all(select_query)
    res = []
    for preview_catalog in preview_catalogs:
        preview_catalog = CatalogData(
            catalog_id=preview_catalog['catalog_id'],
            title=preview_catalog['title'],
            description=preview_catalog['description']
        )

        c_a_items_query = select(catalog_anime).where(catalog_anime.c.catalog_id == preview_catalog.catalog_id)
        catalog_items = await fetch_all(c_a_items_query)
        catalog_items_ids = [anime_item['anime_id'] for anime_item in catalog_items]

        anime_items_query = select(anime) \
            .where(anime.c.anime_id in catalog_items_ids is True)
        anime_items = await fetch_all(anime_items_query)

        preview_catalog.titles = anime_items
        res.append(preview_catalog)

    return res


async def get_catalog_animes(catalog_id: int) -> List[dict[str, Any]] | None:
    select_query = select(catalog).where(catalog.c.catalog_id == catalog_id)
    catalog_item = await fetch_one(select_query)
    catalog_item = CatalogData(
        catalog_id=catalog_item['catalog_id'],
        title=catalog_item['title'],
        description=catalog_item['description']
    )

    c_a_items_query = select(catalog_anime).where(catalog_anime.c.catalog_id == catalog_item.catalog_id)
    catalog_items = await fetch_all(c_a_items_query)
    catalog_items_ids = [anime_item['anime_id'] for anime_item in catalog_items]

    anime_items_query = select(anime) \
        .where(anime.c.anime_id in catalog_items_ids is True)
    anime_items = await fetch_all(anime_items_query)

    return anime_items


async def get_by_id(catalog_id: int) -> dict[str, Any] | None:
    select_query = select(catalog).where(catalog.c.catalog_id == catalog_id)
    return await fetch_one(select_query)
