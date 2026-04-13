import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.storage.db import init_db


if __name__ == "__main__":
    settings = get_settings()
    init_db(settings.database_path)
    print(f"initialized {settings.database_path}")
