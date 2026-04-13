from __future__ import annotations

import sqlite3
from datetime import date
from typing import Iterable

from app.models import ContentItem


def filter_already_pushed(conn: sqlite3.Connection, items: Iterable[ContentItem], receiver_id: str) -> list[ContentItem]:
    pushed_ids = {
        row[0]
        for row in conn.execute(
            "SELECT item_id FROM push_history WHERE receiver_id = ?",
            (receiver_id,),
        ).fetchall()
    }
    return [item for item in items if item.item_id not in pushed_ids]


def save_push_history(
    conn: sqlite3.Connection,
    items: Iterable[ContentItem],
    receiver_id: str,
    status: str,
    message_id: str,
) -> None:
    with conn:
        conn.executemany(
            """
            INSERT INTO push_history (item_id, receiver_id, push_date, status, message_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(item.item_id, receiver_id, date.today().isoformat(), status, message_id) for item in items],
        )
