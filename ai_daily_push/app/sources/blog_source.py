from __future__ import annotations

import hashlib
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import List

from app.models import ContentItem
from app.sources.base import SourceAdapter


class RssSource(SourceAdapter):
    def __init__(self, name: str, feed_url: str) -> None:
        self.name = name
        self.feed_url = feed_url

    def fetch(self) -> List[ContentItem]:
        req = urllib.request.Request(
            self.feed_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = response.read()
        root = ET.fromstring(payload)
        items: List[ContentItem] = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=5)
        for node in root.findall(".//item"):
            title = (node.findtext("title") or "").strip()
            url = (node.findtext("link") or "").strip()
            summary = (node.findtext("description") or "").strip()
            pub_date = (node.findtext("pubDate") or "").strip()
            try:
                published_dt = parsedate_to_datetime(pub_date).astimezone(timezone.utc)
            except Exception:
                published_dt = datetime.now(timezone.utc)
            if published_dt < cutoff:
                continue
            digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
            items.append(
                ContentItem(
                    item_id=digest,
                    item_type="news",
                    source=self.name,
                    title=title,
                    url=url,
                    published_at=published_dt.isoformat(),
                    summary=summary,
                )
            )
        return items


class _AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_anchor = False
        self.href = ""
        self.buffer: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        self.href = attr_map.get("href", "") or ""
        self.buffer = []
        self.in_anchor = True

    def handle_data(self, data: str) -> None:
        if self.in_anchor:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or not self.in_anchor:
            return
        text = " ".join("".join(self.buffer).split())
        if self.href and text:
            self.links.append((self.href, text))
        self.in_anchor = False
        self.href = ""
        self.buffer = []


class AnthropicNewsSource(SourceAdapter):
    name = "anthropic_blog"
    page_url = "https://www.anthropic.com/news"

    def fetch(self) -> List[ContentItem]:
        req = urllib.request.Request(
            self.page_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = response.read().decode("utf-8", errors="ignore")

        parser = _AnchorCollector()
        parser.feed(payload)
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        items: List[ContentItem] = []
        seen_urls: set[str] = set()

        for href, text in parser.links:
            if not href.startswith("/news/"):
                continue
            url = f"https://www.anthropic.com{href}"
            if url in seen_urls:
                continue
            parts = text.split(" ", 4)
            if len(parts) < 5:
                continue
            date_text = " ".join(parts[:3]).replace(" ,", ",")
            try:
                published_dt = datetime.strptime(date_text, "%b %d, %Y").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if published_dt < cutoff:
                continue
            title = parts[4].strip()
            if not title:
                continue
            digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
            items.append(
                ContentItem(
                    item_id=digest,
                    item_type="news",
                    source=self.name,
                    title=title,
                    url=url,
                    published_at=published_dt.isoformat(),
                    summary=text,
                )
            )
            seen_urls.add(url)
            if len(items) >= 20:
                break
        return items


def default_blog_sources() -> list[RssSource]:
    return [
        RssSource("openai_blog", "https://openai.com/news/rss.xml"),
        AnthropicNewsSource(),
        RssSource("deepmind_blog", "https://deepmind.google/blog/rss.xml"),
        RssSource("huggingface_blog", "https://huggingface.co/blog/feed.xml"),
    ]
