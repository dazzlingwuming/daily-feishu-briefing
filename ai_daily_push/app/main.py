from __future__ import annotations

import logging

from app.config import get_settings
from app.logger import configure_logging
from app.models import BriefingItem
from app.pipeline.dedup import dedup_items
from app.pipeline.normalize import normalize_items
from app.pipeline.selector import select_top
from app.pipeline.summarizer import summarize_item
from app.push.renderer import render_daily_report
from app.push.sender import build_sender
from app.sources.arxiv_source import ArxivSource
from app.sources.blog_source import default_blog_sources
from app.storage.content_repo import save_items
from app.storage.db import connect, init_db
from app.storage.push_repo import filter_already_pushed, save_push_history


logger = logging.getLogger(__name__)


def fetch_all():
    settings = get_settings()
    items = []
    try:
        items.extend(ArxivSource().fetch())
    except Exception as exc:
        logger.warning("source fetch failed: %s: %s", "arxiv", exc)
    for source in default_blog_sources():
        if source.name == "openai_blog" and not settings.enable_openai_blog:
            continue
        if source.name == "anthropic_blog" and not settings.enable_anthropic_blog:
            continue
        if source.name == "deepmind_blog" and not settings.enable_deepmind_blog:
            continue
        if source.name == "huggingface_blog" and not settings.enable_hf_blog:
            continue
        try:
            items.extend(source.fetch())
        except Exception as exc:
            logger.warning("source fetch failed: %s: %s", source.name, exc)
    return items


def run_daily_job(ignore_history: bool = False) -> str:
    configure_logging()
    settings = get_settings()
    init_db(settings.database_path)
    conn = connect(settings.database_path)
    all_items = dedup_items(normalize_items(fetch_all()))
    save_items(conn, all_items)
    candidate_items = (
        all_items
        if ignore_history
        else filter_already_pushed(conn, all_items, settings.feishu_receiver_open_id)
    )
    selected_papers = select_top(candidate_items, "paper", settings.paper_top_k)
    selected_news = select_top(candidate_items, "news", settings.news_top_k)
    briefing_papers = [BriefingItem(item, summarize_item(item, settings)) for item in selected_papers]
    briefing_news = [BriefingItem(item, summarize_item(item, settings)) for item in selected_news]
    report = render_daily_report(briefing_papers, briefing_news)
    message_id = build_sender(settings).send_text(report)
    if not ignore_history:
        save_push_history(conn, selected_papers + selected_news, settings.feishu_receiver_open_id, "sent", message_id)
    conn.close()
    return report


if __name__ == "__main__":
    print(run_daily_job())
