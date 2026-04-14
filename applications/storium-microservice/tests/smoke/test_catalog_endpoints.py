import pytest

pytestmark = pytest.mark.integration


def test_featured_products(client, integration_ready):
    r = client.get("/api/catalog/featured")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_catalog_nav(client, integration_ready):
    r = client.get("/api/catalog/nav")
    assert r.status_code == 200


def test_catalog_search_empty_query_rejected(client, integration_ready):
    r = client.get("/api/catalog/search?q=")
    assert r.status_code == 422


def test_catalog_search_valid(client, integration_ready):
    r = client.get("/api/catalog/search?q=test")
    assert r.status_code == 200
