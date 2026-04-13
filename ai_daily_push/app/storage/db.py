from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    return sqlite3.connect(path)


def init_db(path: Path) -> None:
    conn = connect(path)
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS content_cache (
                item_id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                item_type TEXT NOT NULL,
                title TEXT NOT NULL,
                normalized_title TEXT,
                url TEXT NOT NULL,
                published_at TEXT NOT NULL,
                raw_summary TEXT,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS push_history (
                push_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                receiver_id TEXT NOT NULL,
                push_date TEXT NOT NULL,
                status TEXT NOT NULL,
                message_id TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.close()
