import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.push.sender import build_sender


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", default="ai_daily_push smoke test")
    parser.add_argument("--file")
    args = parser.parse_args()
    settings = get_settings()
    if args.file:
        message = Path(args.file).read_text(encoding="utf-8")
    else:
        message = args.message
    message_id = build_sender(settings).send_text(message)
    print(message_id)
