from app.models import BriefingItem, ContentItem, SummaryResult
from app.push.renderer import render_daily_report


def test_render_daily_report():
    item = BriefingItem(
        content=ContentItem("1", "paper", "arxiv", "Test", "https://x", "2026-01-01T00:00:00+00:00", "summary"),
        summary=SummaryResult("brief", ["h1", "h2"], "matters"),
    )
    report = render_daily_report([item], [])
    assert "AI 每日速递" in report
    assert "Test" in report
    assert "matters" in report
