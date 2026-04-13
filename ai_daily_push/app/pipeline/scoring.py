from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models import ContentItem


PAPER_KEYWORDS = ("benchmark", "reasoning", "agent", "multimodal", "inference")
NEWS_KEYWORDS = ("release", "launch", "agent", "developer", "open-source", "api")


def _is_recent(published_at: str, days: int = 1) -> bool:
    try:
        published_dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    return published_dt >= datetime.now(timezone.utc) - timedelta(days=days)


def score_item(item: ContentItem) -> float:
    haystack = f"{item.title} {item.summary}".lower()
    score = 0.0
    if _is_recent(item.published_at, 1):
        score += 3
    if item.item_type == "paper":
        if any(tag in {"cs.AI", "cs.LG", "cs.CL", "stat.ML"} for tag in item.tags):
            score += 2
        if any(keyword in haystack for keyword in PAPER_KEYWORDS):
            score += 2
    else:
        if any(source in item.source for source in ("openai", "anthropic", "deepmind", "huggingface")):
            score += 3
        if any(keyword in haystack for keyword in NEWS_KEYWORDS):
            score += 2
    item.score = score
    return score
