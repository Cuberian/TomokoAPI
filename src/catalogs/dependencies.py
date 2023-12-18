from typing import Any

from src.catalogs import service
from src.exceptions import NotFound


async def valid_catalog_id(catalog_id: int) -> dict[str, Any]:
    catalog = await service.get_by_id(catalog_id)

    if catalog is None:
        raise NotFound()

    return catalog
