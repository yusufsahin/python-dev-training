"""Oturum bazlı Flask sunucu — pytest-playwright base_url için."""

import os
import threading
from typing import Any, Dict, Iterator

import pytest
from werkzeug.serving import make_server

# UI testlerinde adımlar arası gecikme (ms). Ortam: PLAYWRIGHT_UI_SLOWMO=0 hızlandırır.
_DEFAULT_SLOW_MO_MS = 1000


@pytest.fixture(scope="session")
def live_server_url() -> Iterator[str]:
    from app import app as flask_app

    flask_app.config["TESTING"] = True
    server = make_server("127.0.0.1", 0, flask_app, threaded=True)
    port = server.socket.getsockname()[1]
    url = f"http://127.0.0.1:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture(scope="session")
def base_url(live_server_url: str) -> str:
    """pytest-playwright göreli URL'leri bu adrese çözer."""
    return live_server_url


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: Dict[str, Any],
) -> Dict[str, Any]:
    """Yalnızca tests/ui altındaki Playwright testleri — izlemeyi kolaylaştırmak için yavaşlatma."""
    raw = os.environ.get("PLAYWRIGHT_UI_SLOWMO", str(_DEFAULT_SLOW_MO_MS))
    try:
        slow_mo = int(raw)
    except ValueError:
        slow_mo = _DEFAULT_SLOW_MO_MS
    return {**browser_type_launch_args, "slow_mo": slow_mo}
