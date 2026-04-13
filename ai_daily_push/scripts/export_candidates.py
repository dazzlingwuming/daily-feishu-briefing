import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import fetch_all
from app.pipeline.dedup import dedup_items
from app.pipeline.normalize import normalize_items
from app.pipeline.scoring import score_item


def main() -> None:
    items = dedup_items(normalize_items(fetch_all()))
    for item in items:
        score_item(item)
    items = sorted(items, key=lambda x: (x.item_type, -x.score, x.published_at))
    for item in items:
        print(
            json.dumps(
                {
                    "type": item.item_type,
                    "source": item.source,
                    "title": item.title,
                    "published_at": item.published_at,
                    "url": item.url,
                    "score": item.score,
                    "summary": item.summary[:300],
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
