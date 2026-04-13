from __future__ import annotations

from typing import Iterable, List

from app.models import ContentItem
from app.pipeline.scoring import score_item


def select_top(items: Iterable[ContentItem], item_type: str, top_k: int) -> List[ContentItem]:
    filtered = [item for item in items if item.item_type == item_type]
    for item in filtered:
        score_item(item)
    return sorted(filtered, key=lambda item: (item.score, item.published_at), reverse=True)[:top_k]
