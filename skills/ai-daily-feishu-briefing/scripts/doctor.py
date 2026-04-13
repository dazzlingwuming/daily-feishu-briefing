from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


REQUIRED_COMMON = ["FEISHU_RECEIVER_OPEN_ID"]
REQUIRED_API = ["FEISHU_APP_ID", "FEISHU_APP_SECRET"]


def read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def merged_env(env_path: Path | None) -> dict[str, str]:
    values = dict(os.environ)
    if env_path:
        values.update(read_env_file(env_path))
    return values


def check_binary(name: str) -> str:
    path = shutil.which(name)
    return path or ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local prerequisites for the AI daily Feishu briefing workflow.")
    parser.add_argument("--env-file", default=".env", help="Path to a dotenv-style file")
    args = parser.parse_args()

    env_path = Path(args.env_file)
    env = merged_env(env_path)
    send_mode = env.get("FEISHU_SEND_MODE", "cli").strip().lower() or "cli"

    print(f"send_mode={send_mode}")
    print(f"env_file={'present' if env_path.exists() else 'missing'}:{env_path}")

    python_ok = bool(sys.executable)
    codex_path = check_binary("codex")
    lark_cli_path = check_binary("lark-cli")

    print(f"python=ok:{sys.executable if python_ok else 'missing'}")
    print(f"codex={'ok:' + codex_path if codex_path else 'missing'}")
    print(f"lark-cli={'ok:' + lark_cli_path if lark_cli_path else 'missing'}")

    missing = [key for key in REQUIRED_COMMON if not env.get(key)]

    if send_mode == "api":
        missing.extend(key for key in REQUIRED_API if not env.get(key))
    elif send_mode == "cli" and not lark_cli_path:
        missing.append("lark-cli binary")

    if missing:
        print("missing=" + ", ".join(missing))
        return 1

    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
