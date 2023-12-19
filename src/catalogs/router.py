from typing import Any, List, Dict

from src.animes.schemas import AnimeResponse
from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.catalogs.dependencies import valid_catalog_id
from src.catalogs.schemas import CatalogResponse, CatalogData, CatalogItems
from src.catalogs import service
from fastapi import APIRouter,  Depends, status

router = APIRouter()


@router.get("/all", status_code=status.HTTP_201_CREATED, response_model=List[CatalogResponse])
async def get_all_catalogs() -> list[dict[str, Any]] | None:
    catalogs = await service.get_all_catalogs()
    return catalogs


@router.get("/{catalog_id}/info", status_code=status.HTTP_201_CREATED, response_model=CatalogResponse)
async def get_catalog_by_id(catalog=Depends(valid_catalog_id)) -> List[CatalogResponse]:
    return catalog


@router.get("/{catalog_id}/titles", status_code=status.HTTP_201_CREATED, response_model=List[AnimeResponse])
async def get_catalog_by_id(catalog: CatalogResponse = Depends(valid_catalog_id)) -> List[AnimeResponse]:
    animes = await service.get_catalog_animes(catalog['catalog_id'])
    return animes


@router.get("/all/preview", response_model=List[CatalogResponse])
async def get_preview_catalogs() -> List[CatalogResponse]:
    catalogs = await service.get_preview_catalogs()
    return catalogs


@router.post("/create", response_model=CatalogResponse)
async def create_catalog(catalog_data: CatalogData,
                         jwt_data: JWTData = Depends(parse_jwt_user_data)) -> CatalogResponse:
    catalog = await service.create_catalog(catalog_data)
    return CatalogResponse(
        catalog_id=catalog['catalog_id'],
        name=catalog['name'],
        is_preview=catalog['is_preview'],
        description=catalog['description'],
    )


@router.post("/{catalog_id}/add", response_model=CatalogResponse)
async def add_catalog_items(anime_ids: CatalogItems,
                         catalog: int = Depends(valid_catalog_id),
                         jwt_data: JWTData = Depends(parse_jwt_user_data)) -> CatalogResponse:
    animes = await service.add_items(catalog['catalog_id'],anime_ids)
    return CatalogResponse(
        catalog_id=catalog['catalog_id'],
        name=catalog['name'],
        is_preview=catalog['is_preview'],
        description=catalog['description'],
        titles=animes
    )

