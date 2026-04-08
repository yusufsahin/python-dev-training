import re

from modules.catalog.service_provider import get_catalog_service

_CATEGORY_PATH_RE = re.compile(r"^/kategori/([^/]+)/?")


def catalog_nav(request):
    service = get_catalog_service()
    tree = service.get_category_nav_tree()
    active_slug = None
    m = _CATEGORY_PATH_RE.match(request.path)
    if m:
        active_slug = m.group(1)
    return {
        "catalog_nav": tree,
        "catalog_nav_active_slug": active_slug,
    }
