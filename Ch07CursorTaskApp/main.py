"""Görev Yöneticisi masaüstü uygulaması. PyQt6 + SQLite."""
from __future__ import annotations

import sys
import logging

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from database import get_connection, create_tables
from ui.main_window import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    # Veritabanı tablolarını oluştur
    try:
        with get_connection() as conn:
            create_tables(conn)
    except Exception as e:
        logger.exception("Veritabanı başlatılamadı: %s", e)
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("Görev Yöneticisi")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
