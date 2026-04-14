import pytest

pytestmark = pytest.mark.integration

_CART_HEADERS = {"X-Cart-Id": "smoke-test-cart-00000000-0000-4000-8000-000000000001"}


def test_get_cart_requires_header(client, integration_ready):
    r = client.get("/api/cart")
    assert r.status_code == 400


def test_get_cart_with_header(client, integration_ready):
    r = client.get("/api/cart", headers=_CART_HEADERS)
    assert r.status_code == 200


def test_add_to_cart_smoke(client, integration_ready):
    r = client.post(
        "/api/cart/items",
        headers=_CART_HEADERS,
        json={"product_id": 1, "quantity": 1},
    )
    assert r.status_code in (200, 400, 404)
