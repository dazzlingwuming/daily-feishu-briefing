import sys
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import run_daily_job


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ignore-history",
        action="store_true",
        help="Skip push-history filtering for manual verification runs.",
    )
    args = parser.parse_args()
    report = run_daily_job(ignore_history=args.ignore_history)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(report)
