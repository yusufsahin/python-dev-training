"""Ana pencere: menü, toolbar, statusbar, görev listesi, filtre ve arama."""
from __future__ import annotations

import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QStatusBar,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QLabel,
    QFrame,
    QDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

from database import get_connection, create_tables
from database import tasks as tasks_crud
from database import categories as categories_crud
from ui.task_list import TaskListWidget
from ui.task_edit_dialog import TaskEditDialog
from ui.category_dialog import CategoryDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görev Yöneticisi")
        self.setMinimumSize(800, 500)
        self.resize(900, 600)

        self._filters = {
            "status": None,
            "priority": None,
            "category_id": None,
            "search": "",
        }
        self._build_menubar()
        self._build_toolbar()
        self._build_central()
        self._build_statusbar()
        self._refresh_task_list()
        self._refresh_status()

    def _build_menubar(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&Dosya")
        act = QAction("Yeni görev", self)
        act.setShortcut(QKeySequence.StandardKey.New)
        act.triggered.connect(self._new_task)
        file_menu.addAction(act)
        file_menu.addSeparator()
        act = QAction("Dışa aktar (JSON)...", self)
        act.triggered.connect(self._export_json)
        file_menu.addAction(act)
        act = QAction("İçe aktar (JSON)...", self)
        act.triggered.connect(self._import_json)
        file_menu.addAction(act)
        file_menu.addSeparator()
        act = QAction("Çıkış", self)
        act.setShortcut(QKeySequence.StandardKey.Quit)
        act.triggered.connect(self.close)
        file_menu.addAction(act)

        edit_menu = menubar.addMenu("&Düzenle")
        act = QAction("Kategoriler...", self)
        act.triggered.connect(self._manage_categories)
        edit_menu.addAction(act)

        view_menu = menubar.addMenu("&Görünüm")
        act = QAction("Filtreleri göster", self, checkable=True)
        act.setChecked(True)
        act.triggered.connect(self._toggle_filter_visibility)
        view_menu.addAction(act)
        act = QAction("Arama kutusuna odaklan", self)
        act.setShortcut(QKeySequence.StandardKey.Find)
        act.triggered.connect(lambda: self.search_edit.setFocus())
        view_menu.addAction(act)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        act = QAction("Yeni", self)
        act.setShortcut(QKeySequence("Ctrl+N"))
        act.triggered.connect(self._new_task)
        toolbar.addAction(act)
        act = QAction("Düzenle", self)
        act.setShortcut(QKeySequence("Ctrl+E"))
        act.triggered.connect(self._edit_task)
        toolbar.addAction(act)
        act = QAction("Sil", self)
        act.setShortcut(QKeySequence.StandardKey.Delete)
        act.triggered.connect(self._delete_task)
        toolbar.addAction(act)

    def _build_central(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Filtre satırı
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.addWidget(QLabel("Durum:"))
        self.status_combo = QComboBox()
        self.status_combo.addItem("— Tümü —", None)
        for s in ["todo", "in_progress", "done", "cancelled"]:
            label = {"todo": "Yapılacak", "in_progress": "Devam", "done": "Tamamlandı", "cancelled": "İptal"}[s]
            self.status_combo.addItem(label, s)
        self.status_combo.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.status_combo)

        filter_layout.addWidget(QLabel("Öncelik:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItem("— Tümü —", None)
        for p, label in [(1, "Düşük"), (2, "Normal"), (3, "Yüksek"), (4, "Acil")]:
            self.priority_combo.addItem(label, p)
        self.priority_combo.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.priority_combo)

        filter_layout.addWidget(QLabel("Kategori:"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("— Tümü —", None)
        self.category_combo.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.category_combo)

        filter_layout.addWidget(QLabel("Arama:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Başlık veya açıklama...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self._on_search_changed)
        filter_layout.addWidget(self.search_edit, 1)
        self._filter_frame = filter_frame
        layout.addWidget(filter_frame)

        self.task_list = TaskListWidget()
        self.task_list.task_activated.connect(self._edit_task_by_id)
        layout.addWidget(self.task_list)

    def _build_statusbar(self) -> None:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _toggle_filter_visibility(self, checked: bool) -> None:
        self._filter_frame.setVisible(checked)

    def _on_filter_changed(self) -> None:
        self._filters["status"] = self.status_combo.currentData()
        self._filters["priority"] = self.priority_combo.currentData()
        self._filters["category_id"] = self.category_combo.currentData()
        self._refresh_task_list()

    def _on_search_changed(self, text: str) -> None:
        self._filters["search"] = text
        self._refresh_task_list()

    def _refresh_category_combo(self) -> None:
        self.category_combo.blockSignals(True)
        self.category_combo.clear()
        self.category_combo.addItem("— Tümü —", None)
        with get_connection() as conn:
            for row in categories_crud.fetch_all(conn):
                self.category_combo.addItem(row["name"], row["id"])
        self.category_combo.blockSignals(False)

    def _refresh_task_list(self) -> None:
        self._refresh_category_combo()
        with get_connection() as conn:
            rows = tasks_crud.fetch_all(
                conn,
                status_filter=self._filters["status"],
                priority_filter=self._filters["priority"],
                category_id_filter=self._filters["category_id"],
                search_text=self._filters["search"] or None,
            )
        self.task_list.load_tasks(rows)
        self._refresh_status()

    def _refresh_status(self) -> None:
        with get_connection() as conn:
            total, done = tasks_crud.count_by_status(conn)
        self.status_bar.showMessage(f"Toplam: {total}  |  Tamamlanan: {done}")

    def _categories_for_dialog(self) -> list[tuple[int, str]]:
        with get_connection() as conn:
            return [(row["id"], row["name"]) for row in categories_crud.fetch_all(conn)]

    def _new_task(self) -> None:
        categories = self._categories_for_dialog()
        dlg = TaskEditDialog(categories, self, task_id=None, initial={})
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        with get_connection() as conn:
            tasks_crud.insert(
                conn,
                title=dlg.get_title(),
                description=dlg.get_description(),
                priority=dlg.get_priority(),
                status=dlg.get_status(),
                due_date=dlg.get_due_date_iso(),
                category_id=dlg.get_category_id(),
            )
        self._refresh_task_list()

    def _edit_task(self) -> None:
        task_id = self.task_list.selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Bilgi", "Önce bir görev seçin.")
            return
        self._edit_task_by_id(task_id)

    def _edit_task_by_id(self, task_id: int) -> None:
        with get_connection() as conn:
            row = tasks_crud.fetch_by_id(conn, task_id)
        if row is None:
            return
        initial = dict(row)
        categories = self._categories_for_dialog()
        dlg = TaskEditDialog(categories, self, task_id=task_id, initial=initial)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        with get_connection() as conn:
            ok = tasks_crud.update(
                conn,
                task_id,
                title=dlg.get_title(),
                description=dlg.get_description(),
                priority=dlg.get_priority(),
                status=dlg.get_status(),
                due_date=dlg.get_due_date_iso(),
                category_id=dlg.get_category_id(),
            )
        if ok:
            self._refresh_task_list()

    def _delete_task(self) -> None:
        task_id = self.task_list.selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Bilgi", "Önce bir görev seçin.")
            return
        if QMessageBox.question(
            self,
            "Onay",
            "Bu görevi silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        with get_connection() as conn:
            ok = tasks_crud.delete(conn, task_id)
        if ok:
            self._refresh_task_list()

    def _manage_categories(self) -> None:
        dlg = CategoryDialog(get_connection, self)
        dlg.exec()
        self._refresh_task_list()

    def _export_json(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Dışa aktar", "", "JSON (*.json)")
        if not path:
            return
        with get_connection() as conn:
            rows = tasks_crud.fetch_all(conn)
        data = []
        for row in rows:
            data.append({
                "title": row["title"],
                "description": row["description"] or "",
                "priority": row["priority"],
                "status": row["status"],
                "due_date": row["due_date"],
                "category_name": row.get("category_name"),
            })
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.status_bar.showMessage(f"Dışa aktarıldı: {path}")
        except OSError as e:
            QMessageBox.warning(self, "Hata", f"Dosya yazılamadı: {e}")

    def _import_json(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "İçe aktar", "", "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            QMessageBox.warning(self, "Hata", f"Dosya okunamadı veya geçersiz JSON: {e}")
            return
        if not isinstance(data, list):
            QMessageBox.warning(self, "Hata", "JSON bir liste olmalı.")
            return
        count = 0
        with get_connection() as conn:
            for item in data:
                if not isinstance(item, dict) or not item.get("title"):
                    continue
                tasks_crud.insert(
                    conn,
                    title=item["title"],
                    description=item.get("description", ""),
                    priority=int(item.get("priority", 2)),
                    status=item.get("status", "todo"),
                    due_date=item.get("due_date"),
                    category_id=None,
                )
                count += 1
        self._refresh_task_list()
        self.status_bar.showMessage(f"{count} görev içe aktarıldı.")
