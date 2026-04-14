import pytest

pytestmark = pytest.mark.integration


def test_register_validation(client, integration_ready):
    r = client.post("/api/auth/register", json={})
    assert r.status_code == 422


def test_login_wrong_credentials(client, integration_ready):
    r = client.post(
        "/api/auth/login",
        data={"username": "nobody@test.com", "password": "wrong"},
    )
    assert r.status_code in (401, 422)


def test_me_unauthenticated(client, integration_ready):
    r = client.get("/api/auth/me")
    assert r.status_code == 401
