"""Kategori yönetimi: liste, ekle/düzenle/sil, renk seçimi."""
from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QColorDialog,
    QMessageBox,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class CategoryDialog(QDialog):
    """Kategorileri listele, ekle, düzenle, sil."""

    def __init__(self, get_connection, parent=None):
        super().__init__(parent)
        self.get_connection = get_connection
        self.setWindowTitle("Kategori Yönetimi")
        self._build_ui()
        self._load_categories()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self.list_widget)

        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Kategori adı")
        form.addRow("Ad:", self.name_edit)

        self.color_btn = QPushButton("Renk seç")
        self.color_btn.setStyleSheet("background-color: #808080;")
        self._selected_color = "#808080"
        self.color_btn.clicked.connect(self._pick_color)
        form.addRow("Renk:", self.color_btn)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Ekle")
        self.add_btn.clicked.connect(self._add_category)
        self.edit_btn = QPushButton("Düzenle")
        self.edit_btn.clicked.connect(self._edit_category)
        self.delete_btn = QPushButton("Sil")
        self.delete_btn.clicked.connect(self._delete_category)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self._on_selection_changed()

    def _pick_color(self) -> None:
        color = QColorDialog.getColor(QColor(self._selected_color), self, "Kategori rengi")
        if color.isValid():
            self._selected_color = color.name()
            self.color_btn.setStyleSheet(f"background-color: {self._selected_color};")

    def _load_categories(self) -> None:
        self.list_widget.clear()
        with self.get_connection() as conn:
            from database import categories as categories_crud
            rows = categories_crud.fetch_all(conn)
        for row in rows:
            item = QListWidgetItem(row["name"])
            item.setData(Qt.ItemDataRole.UserRole, {"id": row["id"], "name": row["name"], "color": row["color"] or "#808080"})
            if row.get("color"):
                item.setForeground(QColor(row["color"]))
            self.list_widget.addItem(item)

    def _on_selection_changed(self) -> None:
        current = self.list_widget.currentItem()
        has_selection = current is not None
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        if current is not None:
            data = current.data(Qt.ItemDataRole.UserRole) or {}
            self.name_edit.setText(data.get("name", ""))
            self._selected_color = data.get("color", "#808080")
            self.color_btn.setStyleSheet(f"background-color: {self._selected_color};")
        else:
            self.name_edit.clear()
            self._selected_color = "#808080"
            self.color_btn.setStyleSheet("background-color: #808080;")

    def _add_category(self) -> None:
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setFocus()
            return
        with self.get_connection() as conn:
            from database import categories as categories_crud
            try:
                categories_crud.insert(conn, name, self._selected_color)
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Eklenemedi: {e}")
                return
        self.name_edit.clear()
        self._selected_color = "#808080"
        self.color_btn.setStyleSheet("background-color: #808080;")
        self._load_categories()

    def _edit_category(self) -> None:
        current = self.list_widget.currentItem()
        if not current:
            return
        data = current.data(Qt.ItemDataRole.UserRole) or {}
        cat_id = data.get("id")
        if cat_id is None:
            return
        name = self.name_edit.text().strip()
        if not name:
            self.name_edit.setFocus()
            return
        with self.get_connection() as conn:
            from database import categories as categories_crud
            ok = categories_crud.update(conn, cat_id, name, self._selected_color)
            if not ok:
                QMessageBox.warning(self, "Hata", "Güncellenemedi.")
                return
        self._load_categories()

    def _delete_category(self) -> None:
        current = self.list_widget.currentItem()
        if not current:
            return
        data = current.data(Qt.ItemDataRole.UserRole) or {}
        cat_id = data.get("id")
        if cat_id is None:
            return
        if QMessageBox.question(
            self,
            "Onay",
            "Bu kategori silinecek. Görevlerdeki atama kaldırılacak. Devam?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        with self.get_connection() as conn:
            from database import categories as categories_crud
            categories_crud.delete(conn, cat_id)
        self._load_categories()
