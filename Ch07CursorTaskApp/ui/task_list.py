"""Görev tablosu widget'ı: liste, sıralama, seçim sinyalleri."""
from __future__ import annotations

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

# database modülünden sabitler (döngüsel import önlemek için burada da kullanılabilir)
PRIORITY_LOW, PRIORITY_NORMAL, PRIORITY_HIGH, PRIORITY_URGENT = 1, 2, 3, 4
STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE, STATUS_CANCELLED = "todo", "in_progress", "done", "cancelled"

PRIORITY_LABELS = {1: "Düşük", 2: "Normal", 3: "Yüksek", 4: "Acil"}
STATUS_LABELS = {
    "todo": "Yapılacak",
    "in_progress": "Devam",
    "done": "Tamamlandı",
    "cancelled": "İptal",
}


class TaskListWidget(QTableWidget):
    """Görev listesini gösteren tablo. Çift tıklama ve seçim değişimi sinyalleri yayar."""

    task_activated = pyqtSignal(int)  # task_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Başlık", "Öncelik", "Durum", "Son Tarih", "Kategori", "Id"])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)
        self.setColumnHidden(5, True)  # id gizli
        self._rows_by_id: dict[int, int] = {}  # task_id -> table row index (sorting sonrası güncellenir)

        self.cellDoubleClicked.connect(self._on_cell_double_clicked)

    def _on_cell_double_clicked(self, row: int, _col: int) -> None:
        id_item = self.item(row, 5)
        if id_item is not None:
            try:
                task_id = int(id_item.text())
                self.task_activated.emit(task_id)
            except ValueError:
                pass

    def selected_task_id(self) -> int | None:
        """Seçili satırdaki görev id'sini döndürür; seçim yoksa None."""
        row = self.currentRow()
        if row < 0:
            return None
        id_item = self.item(row, 5)
        if id_item is None:
            return None
        try:
            return int(id_item.text())
        except ValueError:
            return None

    def load_tasks(self, rows: list) -> None:
        """Veritabanı satırları (sqlite3.Row veya dict) ile tabloyu doldurur."""
        self.setSortingEnabled(False)
        self.setRowCount(len(rows))
        self._rows_by_id.clear()
        for i, row in enumerate(rows):
            r = dict(row) if hasattr(row, "keys") else (row if isinstance(row, dict) else {})
            task_id = r.get("id")
            if task_id is not None:
                self._rows_by_id[int(task_id)] = i
            self.setItem(i, 0, QTableWidgetItem(str(r.get("title", ""))))
            self.setItem(i, 1, QTableWidgetItem(PRIORITY_LABELS.get(r.get("priority"), str(r.get("priority", "")))))
            self.setItem(i, 2, QTableWidgetItem(STATUS_LABELS.get(r.get("status"), str(r.get("status", "")))))
            self.setItem(i, 3, QTableWidgetItem(str(r.get("due_date") or "")))
            self.setItem(i, 4, QTableWidgetItem(str(r.get("category_name") or "")))
            id_item = QTableWidgetItem(str(r.get("id", "")))
            id_item.setData(Qt.ItemDataRole.UserRole, r.get("id"))
            self.setItem(i, 5, id_item)
        self.setSortingEnabled(True)

    def clear_list(self) -> None:
        """Tabloyu temizler."""
        self.setSortingEnabled(False)
        self.setRowCount(0)
        self._rows_by_id.clear()
        self.setSortingEnabled(True)
