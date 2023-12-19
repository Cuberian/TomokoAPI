from typing import Any, List

from fastapi import Depends
from sqlalchemy import insert, select

from src.catalogs.schemas import CatalogResponse, CatalogData, CatalogItems
from src.database import fetch_all, fetch_one, catalog, anime, catalog_anime
from src.exceptions import NotFound
from src.animes import service as anime_service


async def get_all_catalogs() -> List[dict[str, Any]] | None:
    select_query = select(catalog)
    return await fetch_all(select_query)


async def get_preview_catalogs() -> List[CatalogResponse] | None:
    select_query = select(catalog).where(catalog.c.is_preview == True)
    preview_catalogs = await fetch_all(select_query)
    res = []
    for preview_catalog in preview_catalogs:
        preview_catalog = CatalogResponse(
            catalog_id=preview_catalog['catalog_id'],
            name=preview_catalog['name'],
            description=preview_catalog['description'],
            is_preview=True
        )
        anime_items = await get_catalog_animes(preview_catalog.catalog_id)
        preview_catalog.titles = anime_items
        res.append(preview_catalog)

    return res


async def get_catalog_animes(catalog_id: int) -> List[dict[str, Any]] | None:
    c_a_items_query = select(catalog_anime).where(catalog_anime.c.catalog_id == catalog_id)
    catalog_items = await fetch_all(c_a_items_query)
    catalog_items_ids = (anime_item['anime_id'] for anime_item in catalog_items)

    anime_items_query = select(anime) \
        .where(anime.c.anime_id.in_(catalog_items_ids))
    anime_items = await fetch_all(anime_items_query)

    return anime_items


async def get_by_id(catalog_id: int) -> dict[str, Any] | None:
    select_query = select(catalog).where(catalog.c.catalog_id == catalog_id)
    return await fetch_one(select_query)


async def create_catalog(catalog_data: CatalogData) -> dict[str, Any] | None:
    insert_query = (
        insert(catalog)
        .values(
            {
                "name": catalog_data.name,
                "is_preview": catalog_data.is_preview,
                "description": catalog_data.description,
            }
        )
        .returning(catalog)
    )

    return await fetch_one(insert_query)


async def add_items(catalog_id: int, catalog_items: CatalogItems) -> List[dict[str, Any]] | None:
    res = []

    for item in catalog_items.items_ids:
        anime_item = await anime_service.get_by_id(item)

        if anime_item is None:
            raise NotFound()

        insert_query = (
            insert(catalog_anime)
            .values(
                {
                    "catalog_id": catalog_id,
                    "anime_id": anime_item['anime_id'],
                }
            )
            .returning(catalog_anime)
        )

        await fetch_one(insert_query)
        res.append(anime_item)

    return res
