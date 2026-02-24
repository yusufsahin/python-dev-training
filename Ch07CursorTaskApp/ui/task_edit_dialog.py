"""Görev ekleme/düzenleme formu."""
from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QPushButton,
    QDialogButtonBox,
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QKeySequence
from datetime import datetime

from database.tasks import (
    PRIORITY_LOW,
    PRIORITY_NORMAL,
    PRIORITY_HIGH,
    PRIORITY_URGENT,
    STATUS_TODO,
    STATUS_IN_PROGRESS,
    STATUS_DONE,
    STATUS_CANCELLED,
)

PRIORITY_LABELS = [
    (PRIORITY_LOW, "Düşük"),
    (PRIORITY_NORMAL, "Normal"),
    (PRIORITY_HIGH, "Yüksek"),
    (PRIORITY_URGENT, "Acil"),
]
STATUS_LABELS = [
    (STATUS_TODO, "Yapılacak"),
    (STATUS_IN_PROGRESS, "Devam"),
    (STATUS_DONE, "Tamamlandı"),
    (STATUS_CANCELLED, "İptal"),
]


class TaskEditDialog(QDialog):
    """Görev ekleme veya düzenleme diyaloğu."""

    def __init__(self, categories: list, parent=None, task_id: int | None = None, initial: dict | None = None):
        super().__init__(parent)
        self.task_id = task_id
        self.initial = initial or {}
        self.categories = categories  # [(id, name), ...]
        self.setWindowTitle("Görev Düzenle" if task_id else "Yeni Görev")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Başlık")
        self.title_edit.setMaxLength(500)
        form.addRow("Başlık:", self.title_edit)

        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Açıklama (isteğe bağlı)")
        self.desc_edit.setMaximumHeight(100)
        form.addRow("Açıklama:", self.desc_edit)

        self.priority_combo = QComboBox()
        for val, label in PRIORITY_LABELS:
            self.priority_combo.addItem(label, val)
        form.addRow("Öncelik:", self.priority_combo)

        self.status_combo = QComboBox()
        for val, label in STATUS_LABELS:
            self.status_combo.addItem(label, val)
        form.addRow("Durum:", self.status_combo)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setSpecialValueText("—")  # null yerine
        self.due_date_edit.setDate(QDate(2000, 1, 1))  # minimum
        form.addRow("Son Tarih:", self.due_date_edit)

        self.category_combo = QComboBox()
        self.category_combo.addItem("— Kategori yok —", None)
        for cat_id, cat_name in self.categories:
            self.category_combo.addItem(str(cat_name), cat_id)
        form.addRow("Kategori:", self.category_combo)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._load_initial()

    def _load_initial(self) -> None:
        if not self.initial:
            return
        self.title_edit.setText(self.initial.get("title", ""))
        self.desc_edit.setPlainText(self.initial.get("description", ""))
        idx = self.priority_combo.findData(self.initial.get("priority", PRIORITY_NORMAL))
        if idx >= 0:
            self.priority_combo.setCurrentIndex(idx)
        idx = self.status_combo.findData(self.initial.get("status", STATUS_TODO))
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)
        due = self.initial.get("due_date")
        if due:
            try:
                dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
                self.due_date_edit.setDate(QDate(dt.year, dt.month, dt.day))
            except (ValueError, TypeError):
                self.due_date_edit.setDate(QDate(2000, 1, 1))
        else:
            self.due_date_edit.setDate(QDate(2000, 1, 1))
        cat_id = self.initial.get("category_id")
        idx = self.category_combo.findData(cat_id)
        if idx >= 0:
            self.category_combo.setCurrentIndex(idx)

    def get_title(self) -> str:
        return self.title_edit.text().strip()

    def get_description(self) -> str:
        return self.desc_edit.toPlainText().strip()

    def get_priority(self) -> int:
        return self.priority_combo.currentData() or PRIORITY_NORMAL

    def get_status(self) -> str:
        return self.status_combo.currentData() or STATUS_TODO

    def get_due_date_iso(self) -> str | None:
        qd = self.due_date_edit.date()
        if qd.year() <= 2000 and qd.month() == 1 and qd.day() == 1:
            return None
        return f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}"

    def get_category_id(self) -> int | None:
        return self.category_combo.currentData()

    def accept(self) -> None:
        if not self.get_title():
            self.title_edit.setFocus()
            return
        super().accept()
