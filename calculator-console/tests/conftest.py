"""Ortak fixture ve proje kök yolu."""

from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def main_py(project_root: Path) -> Path:
    return project_root / "main.py"
