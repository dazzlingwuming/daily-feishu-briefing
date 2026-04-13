from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ContentItem:
    item_id: str
    item_type: str
    source: str
    title: str
    url: str
    published_at: str
    summary: str
    authors: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    raw_text: Optional[str] = None
    score: float = 0.0
    normalized_title: str = ""


@dataclass
class SummaryResult:
    brief: str
    highlights: List[str]
    why_it_matters: str


@dataclass
class BriefingItem:
    content: ContentItem
    summary: SummaryResult
