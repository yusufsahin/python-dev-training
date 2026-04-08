from core.repositories.catalog_repository import DjangoCategoryRepository, DjangoProductRepository
from core.services.catalog_service import CatalogService


def get_catalog_service() -> CatalogService:
    return CatalogService(
        category_repo=DjangoCategoryRepository(),
        product_repo=DjangoProductRepository(),
    )
