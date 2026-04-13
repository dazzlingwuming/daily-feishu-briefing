# Architecture

## Goal

Build or maintain a daily pipeline that:

1. collects AI papers and official AI news
2. normalizes and deduplicates items
3. selects the most relevant items
4. generates structured Chinese summaries
5. pushes a daily briefing to Feishu private chat
6. stores history to avoid duplicate delivery

## Default Layers

- `sources/`: fetch raw content one source at a time
- `pipeline/`: normalize, dedup, score, select, summarize
- `push/`: render and send
- `storage/`: SQLite persistence
- `scripts/`: one-off operational helpers

## Default Models

```python
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
```

```python
from dataclasses import dataclass
from typing import List

@dataclass
class SummaryResult:
    brief: str
    highlights: List[str]
    why_it_matters: str
```

## Source Policy

Start narrow and stable.

- Prefer official feeds, APIs, or structured pages.
- Do not start with a generic scraping framework.
- Write one adapter per source.
- Add timeouts and simple retries.
- Degrade gracefully if fields are missing.

## Dedup Policy

Apply all three layers:

1. Exact URL dedup
2. Normalized title dedup
3. Push history dedup

## Ranking Defaults

### Papers

- Fresh within 24 hours: high boost
- Matches target categories: boost
- Contains keywords such as `benchmark`, `reasoning`, `agent`, `multimodal`, `inference`: boost

### News

- Official source: high boost
- Fresh within 24 hours: high boost
- Model launch, product launch, open-source release: boost
- Developer tooling or enterprise AI relevance: boost

## Storage

Use SQLite by default.

Minimum tables:

- `content_cache`
- `push_history`

`push_history` should include `message_id` when available for easier debugging.
