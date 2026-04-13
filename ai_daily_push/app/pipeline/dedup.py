from __future__ import annotations

from typing import Iterable, List, Set

from app.models import ContentItem


def dedup_items(items: Iterable[ContentItem]) -> List[ContentItem]:
    seen_urls: Set[str] = set()
    seen_titles: Set[str] = set()
    output: List[ContentItem] = []
    for item in items:
        if item.url in seen_urls:
            continue
        if item.normalized_title and item.normalized_title in seen_titles:
            continue
        seen_urls.add(item.url)
        if item.normalized_title:
            seen_titles.add(item.normalized_title)
        output.append(item)
    return output
