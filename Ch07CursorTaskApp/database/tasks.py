"""tasks tablosu CRUD işlemleri."""
from __future__ import annotations

import sqlite3
from datetime import datetime

# Öncelik: 1=düşük, 2=normal, 3=yüksek, 4=acil
PRIORITY_LOW = 1
PRIORITY_NORMAL = 2
PRIORITY_HIGH = 3
PRIORITY_URGENT = 4

# Durumlar
STATUS_TODO = "todo"
STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"
STATUS_CANCELLED = "cancelled"

PRIORITIES = (PRIORITY_LOW, PRIORITY_NORMAL, PRIORITY_HIGH, PRIORITY_URGENT)
STATUSES = (STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE, STATUS_CANCELLED)


def _now_iso() -> str:
    return datetime.now().isoformat()


def insert(
    conn: sqlite3.Connection,
    title: str,
    description: str = "",
    priority: int = PRIORITY_NORMAL,
    status: str = STATUS_TODO,
    due_date: str | None = None,
    category_id: int | None = None,
) -> int:
    """Yeni görev ekler; eklenen kaydın id'sini döndürür."""
    now = _now_iso()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO tasks (title, description, priority, status, due_date, category_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, description or "", priority, status, due_date, category_id, now, now),
        )
        return cur.lastrowid or 0
    finally:
        cur.close()


def fetch_all(
    conn: sqlite3.Connection,
    status_filter: str | None = None,
    priority_filter: int | None = None,
    category_id_filter: int | None = None,
    search_text: str | None = None,
) -> list[sqlite3.Row]:
    """Tüm görevleri döndürür; isteğe bağlı filtreler uygulanır."""
    cur = conn.cursor()
    try:
        sql = """
            SELECT t.id, t.title, t.description, t.priority, t.status, t.due_date,
                   t.category_id, t.created_at, t.updated_at, c.name AS category_name, c.color AS category_color
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params: list = []
        if status_filter:
            sql += " AND t.status = ?"
            params.append(status_filter)
        if priority_filter is not None:
            sql += " AND t.priority = ?"
            params.append(priority_filter)
        if category_id_filter is not None:
            sql += " AND t.category_id = ?"
            params.append(category_id_filter)
        if search_text and search_text.strip():
            sql += " AND (t.title LIKE ? OR t.description LIKE ?)"
            pattern = f"%{search_text.strip()}%"
            params.extend([pattern, pattern])
        sql += " ORDER BY t.priority DESC, (t.due_date IS NULL), t.due_date ASC, t.created_at DESC"
        cur.execute(sql, params)
        return list(cur.fetchall())
    finally:
        cur.close()


def fetch_by_id(conn: sqlite3.Connection, task_id: int) -> sqlite3.Row | None:
    """Belirtilen id'deki görevi döndürür."""
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT t.id, t.title, t.description, t.priority, t.status, t.due_date,
                      t.category_id, t.created_at, t.updated_at, c.name AS category_name, c.color AS category_color
               FROM tasks t LEFT JOIN categories c ON t.category_id = c.id
               WHERE t.id = ?""",
            (task_id,),
        )
        return cur.fetchone()
    finally:
        cur.close()


def update(
    conn: sqlite3.Connection,
    task_id: int,
    title: str,
    description: str = "",
    priority: int = PRIORITY_NORMAL,
    status: str = STATUS_TODO,
    due_date: str | None = None,
    category_id: int | None = None,
) -> bool:
    """Görevi günceller. Kayıt yoksa False döner."""
    now = _now_iso()
    cur = conn.cursor()
    try:
        cur.execute(
            """UPDATE tasks SET title=?, description=?, priority=?, status=?, due_date=?, category_id=?, updated_at=?
               WHERE id=?""",
            (title, description or "", priority, status, due_date, category_id, now, task_id),
        )
        return cur.rowcount > 0
    finally:
        cur.close()


def delete(conn: sqlite3.Connection, task_id: int) -> bool:
    """Görevi siler. Kayıt yoksa False döner."""
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        return cur.rowcount > 0
    finally:
        cur.close()


def count_by_status(conn: sqlite3.Connection) -> tuple[int, int]:
    """(toplam_görev, tamamlanan_görev) döndürür."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM tasks")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", (STATUS_DONE,))
        done = cur.fetchone()[0]
        return total, done
    finally:
        cur.close()
