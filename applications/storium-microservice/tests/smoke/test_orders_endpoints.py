import pytest

pytestmark = pytest.mark.integration

_CART_HEADERS = {"X-Cart-Id": "smoke-test-orders-0000-0000-4000-8000-000000000002"}


def test_checkout_unauthenticated(client, integration_ready):
    r = client.post(
        "/api/orders/checkout",
        headers=_CART_HEADERS,
        json={
            "shipping_name": "x",
            "shipping_address": "y",
            "shipping_city": "z",
            "shipping_phone": "1",
        },
    )
    assert r.status_code == 401


def test_list_orders_unauthenticated(client, integration_ready):
    r = client.get("/api/orders")
    assert r.status_code == 401
