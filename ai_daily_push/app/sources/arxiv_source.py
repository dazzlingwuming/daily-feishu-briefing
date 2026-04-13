from __future__ import annotations

import hashlib
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

from app.config import get_settings
from app.models import ContentItem
from app.sources.base import SourceAdapter


class ArxivSource(SourceAdapter):
    name = "arxiv"
    categories = ("cs.AI", "cs.LG", "cs.CL", "stat.ML")
    _rate_file = Path(__file__).resolve().parents[2] / ".arxiv_last_request"

    def _wait_for_rate_limit(self) -> None:
        if not self._rate_file.exists():
            return
        try:
            previous = float(self._rate_file.read_text(encoding="utf-8").strip())
        except ValueError:
            return
        delta = time.time() - previous
        if delta < 3.2:
            time.sleep(3.2 - delta)

    def _mark_request(self) -> None:
        self._rate_file.write_text(str(time.time()), encoding="utf-8")

    def _user_agent(self) -> str:
        settings = get_settings()
        email = settings.arxiv_contact_email.strip()
        base = "ai_daily_push/0.1"
        return f"{base} ({email})" if email else base

    def _fetch_feed(self, url: str) -> bytes:
        last_error: Exception | None = None
        for attempt in range(4):
            self._wait_for_rate_limit()
            req = urllib.request.Request(
                url,
                headers={"User-Agent": self._user_agent()},
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    payload = response.read()
                self._mark_request()
                return payload
            except urllib.error.HTTPError as exc:
                self._mark_request()
                last_error = exc
                if exc.code == 429:
                    retry_after = exc.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after and retry_after.isdigit() else 5.0 * (attempt + 1)
                    time.sleep(delay)
                    continue
                raise
            except Exception as exc:
                self._mark_request()
                last_error = exc
                time.sleep(2.0 * (attempt + 1))
        raise RuntimeError(f"arXiv fetch failed after retries: {last_error}")

    def fetch(self) -> List[ContentItem]:
        query = " OR ".join(f"cat:{category}" for category in self.categories)
        params = urllib.parse.urlencode(
            {
                "search_query": query,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "start": 0,
                "max_results": 20,
            }
        )
        url = f"http://export.arxiv.org/api/query?{params}"
        xml_data = self._fetch_feed(url)
        root = ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items: List[ContentItem] = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=3)
        for entry in root.findall("atom:entry", ns):
            published = entry.findtext("atom:published", default="", namespaces=ns)
            published_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if published_dt < cutoff:
                continue
            title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
            summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split())
            entry_url = ""
            for link in entry.findall("atom:link", ns):
                if link.attrib.get("rel") == "alternate":
                    entry_url = link.attrib.get("href", "")
                    break
            authors = [
                author.findtext("atom:name", default="", namespaces=ns)
                for author in entry.findall("atom:author", ns)
            ]
            tags = [category.attrib.get("term", "") for category in entry.findall("atom:category", ns)]
            digest = hashlib.sha1(entry_url.encode("utf-8")).hexdigest()
            items.append(
                ContentItem(
                    item_id=digest,
                    item_type="paper",
                    source=self.name,
                    title=title,
                    url=entry_url,
                    published_at=published_dt.isoformat(),
                    summary=summary,
                    authors=[name for name in authors if name],
                    tags=[tag for tag in tags if tag],
                )
            )
        return items
