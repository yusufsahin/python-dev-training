"""Smoke / integration: monolit TestClient veya Traefik gateway (STORIUM_GATEWAY_URL)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")


class _HttpxCompatResponse:
    def __init__(self, raw: Any) -> None:
        self._raw = raw

    @property
    def status_code(self) -> int:
        return self._raw.status_code

    def json(self) -> Any:
        return self._raw.json()


class _GatewayClient:
    def __init__(self, base_url: str) -> None:
        import httpx

        self._client = httpx.Client(base_url=base_url.rstrip("/"), timeout=30.0)

    def get(self, url: str, **kwargs: Any) -> _HttpxCompatResponse:
        return _HttpxCompatResponse(self._client.get(url, **kwargs))

    def post(self, url: str, **kwargs: Any) -> _HttpxCompatResponse:
        return _HttpxCompatResponse(self._client.post(url, **kwargs))

    def patch(self, url: str, **kwargs: Any) -> _HttpxCompatResponse:
        return _HttpxCompatResponse(self._client.patch(url, **kwargs))

    def delete(self, url: str, **kwargs: Any) -> _HttpxCompatResponse:
        return _HttpxCompatResponse(self._client.delete(url, **kwargs))

    def close(self) -> None:
        self._client.close()


def _database_reachable() -> bool:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        return False
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
    except OSError:
        return False
    except Exception:
        return False
    return True


def _redis_reachable() -> bool:
    try:
        import redis as redis_lib
    except ImportError:
        return False
    url = os.getenv("REDIS_URL", "redis://localhost:6379/1").strip()
    try:
        r = redis_lib.Redis.from_url(url, decode_responses=True)
        r.ping()
        r.close()
    except Exception:
        return False
    return True


def _gateway_reachable(url: str) -> bool:
    try:
        import httpx

        r = httpx.get(f"{url.rstrip('/')}/api/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


@pytest.fixture
def client():
    gateway = os.getenv("STORIUM_GATEWAY_URL", "").strip()
    if gateway:
        g = _GatewayClient(gateway)
        try:
            yield g
        finally:
            g.close()
        return

    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def integration_ready():
    gateway = os.getenv("STORIUM_GATEWAY_URL", "").strip()
    if gateway:
        if not _gateway_reachable(gateway):
            pytest.skip("STORIUM_GATEWAY_URL erişilemiyor (docker compose + Traefik çalışıyor mu?)")
        return
    if not _database_reachable():
        pytest.skip("PostgreSQL erişilemiyor (.env içinde DATABASE_URL ve migrasyonlar)")
    if not _redis_reachable():
        pytest.skip("Redis erişilemiyor (.env içinde REDIS_URL)")
