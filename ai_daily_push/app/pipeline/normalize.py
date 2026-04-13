from __future__ import annotations

import re
from typing import Iterable, List

from app.models import ContentItem


def normalize_title(title: str) -> str:
    title = title.lower().strip()
    title = re.sub(r"[^a-z0-9\u4e00-\u9fa5 ]+", " ", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def normalize_items(items: Iterable[ContentItem]) -> List[ContentItem]:
    normalized: List[ContentItem] = []
    for item in items:
        item.title = " ".join(item.title.split())
        item.summary = " ".join(item.summary.split())
        item.normalized_title = normalize_title(item.title)
        normalized.append(item)
    return normalized
