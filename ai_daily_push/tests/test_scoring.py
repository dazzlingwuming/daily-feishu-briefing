from app.models import ContentItem
from app.pipeline.scoring import score_item


def test_score_item_positive_for_recent_official_news():
    item = ContentItem(
        item_id="1",
        item_type="news",
        source="openai_blog",
        title="OpenAI release for developers",
        url="https://x",
        published_at="2099-01-01T00:00:00+00:00",
        summary="new API release",
    )
    assert score_item(item) >= 5
