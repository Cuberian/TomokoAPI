from typing import Any, List, Dict

from src.animes.schemas import AnimeResponse
from src.catalogs.dependencies import valid_catalog_id
from src.catalogs.schemas import CatalogData
from src.catalogs import service
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_201_CREATED, response_model=List[CatalogData])
async def get_all_catalogs() -> list[dict[str, Any]] | None:
    catalogs = await service.get_all_catalogs()
    return catalogs


@router.get("/{catalog_id}", status_code=status.HTTP_201_CREATED, response_model=List[CatalogData])
async def get_catalog_by_id(catalog=Depends(valid_catalog_id)) -> List[CatalogData]:
    return catalog


@router.get("/{catalog_id}/titles", status_code=status.HTTP_201_CREATED, response_model=List[AnimeResponse])
async def get_catalog_by_id(catalog: CatalogData = Depends(valid_catalog_id)) -> List[AnimeResponse]:
    animes = await service.get_catalog_animes(catalog.catalog_id)
    return animes


@router.get("/preview", response_model=List[CatalogData])
async def get_preview_catalogs() -> dict[str, str]:
    catalogs = await service.get_preview_catalogs()
    return catalogs
