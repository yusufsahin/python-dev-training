"""categories tablosu CRUD işlemleri."""
from __future__ import annotations

import sqlite3

DEFAULT_COLOR = "#808080"


def insert(conn: sqlite3.Connection, name: str, color: str = DEFAULT_COLOR) -> int:
    """Yeni kategori ekler; eklenen kaydın id'sini döndürür."""
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name, color) VALUES (?, ?)", (name.strip(), color or DEFAULT_COLOR))
        return cur.lastrowid or 0
    finally:
        cur.close()


def fetch_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Tüm kategorileri döndürür."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, color FROM categories ORDER BY name")
        return list(cur.fetchall())
    finally:
        cur.close()


def fetch_by_id(conn: sqlite3.Connection, category_id: int) -> sqlite3.Row | None:
    """Belirtilen id'deki kategoriyi döndürür."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, color FROM categories WHERE id = ?", (category_id,))
        return cur.fetchone()
    finally:
        cur.close()


def update(conn: sqlite3.Connection, category_id: int, name: str, color: str = DEFAULT_COLOR) -> bool:
    """Kategoriyi günceller. Kayıt yoksa False döner."""
    cur = conn.cursor()
    try:
        cur.execute("UPDATE categories SET name=?, color=? WHERE id=?", (name.strip(), color or DEFAULT_COLOR, category_id))
        return cur.rowcount > 0
    finally:
        cur.close()


def delete(conn: sqlite3.Connection, category_id: int) -> bool:
    """Kategoriyi siler. Kayıt yoksa False döner. Görevlerdeki category_id null kalabilir veya siz güncelleyebilirsiniz."""
    cur = conn.cursor()
    try:
        cur.execute("UPDATE tasks SET category_id = NULL WHERE category_id = ?", (category_id,))
        cur.execute("DELETE FROM categories WHERE id=?", (category_id,))
        return cur.rowcount > 0
    finally:
        cur.close()
