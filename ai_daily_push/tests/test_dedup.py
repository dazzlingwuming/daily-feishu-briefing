from app.models import ContentItem
from app.pipeline.dedup import dedup_items
from app.pipeline.normalize import normalize_items


def test_dedup_by_url_and_title():
    items = normalize_items(
        [
            ContentItem("1", "news", "a", "Hello World", "https://a", "2026-01-01T00:00:00+00:00", "x"),
            ContentItem("2", "news", "b", "Hello   World!", "https://b", "2026-01-01T00:00:00+00:00", "y"),
            ContentItem("3", "news", "c", "Other", "https://a", "2026-01-01T00:00:00+00:00", "z"),
        ]
    )
    deduped = dedup_items(items)
    assert len(deduped) == 1
