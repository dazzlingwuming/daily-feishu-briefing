from __future__ import annotations

import sqlite3
from typing import Iterable

from app.models import ContentItem


def save_items(conn: sqlite3.Connection, items: Iterable[ContentItem]) -> None:
    with conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO content_cache
            (item_id, source, item_type, title, normalized_title, url, published_at, raw_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item.item_id,
                    item.source,
                    item.item_type,
                    item.title,
                    item.normalized_title,
                    item.url,
                    item.published_at,
                    item.summary,
                )
                for item in items
            ],
        )
