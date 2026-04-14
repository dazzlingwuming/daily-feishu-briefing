from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_ENV_FILE = Path(__file__).resolve().parents[1] / "ai_daily_push" / ".env"


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


def load_env(path: Path | None) -> dict[str, str]:
    env = dict(os.environ)
    if path and path.exists():
        env.update(read_env_file(path))
    return env


def build_post_payload(message: str) -> dict[str, object]:
    lines = [line.rstrip() for line in message.splitlines()]
    title = next((line for line in lines if line.strip()), "AI 每日速递")
    content: list[list[dict[str, str]]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        if line.startswith("链接："):
            url = line[len("链接：") :].strip()
            content.append(
                [
                    {"tag": "text", "text": "链接："},
                    {"tag": "a", "text": url, "href": url},
                ]
            )
        else:
            content.append([{"tag": "text", "text": line}])
    return {"zh_cn": {"title": title, "content": content or [[{"tag": "text", "text": title}]]}}


def send_message(receiver: str, message: str) -> int:
    cli = shutil.which("lark-cli") or shutil.which("lark-cli.cmd") or shutil.which("lark-cli.CMD")
    if not cli:
        raise SystemExit("lark-cli is not available in PATH")

    cmd = [
        cli,
        "im",
        "+messages-send",
        "--as",
        "bot",
        "--user-id",
        receiver,
    ]

    if "\n" in message:
        payload = build_post_payload(message)
        cmd.extend(["--msg-type", "post", "--content", json.dumps(payload, ensure_ascii=False)])
    else:
        cmd.extend(["--text", message])

    result = subprocess.run(cmd, text=True, capture_output=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a UTF-8 briefing file to Feishu using lark-cli.")
    parser.add_argument("--file", required=True, help="Path to the UTF-8 text file to send")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE), help="Dotenv-style file with FEISHU_RECEIVER_OPEN_ID")
    args = parser.parse_args()

    env = load_env(Path(args.env_file))
    receiver = env.get("FEISHU_RECEIVER_OPEN_ID", "").strip()
    if not receiver:
        raise SystemExit("FEISHU_RECEIVER_OPEN_ID is required")

    message = Path(args.file).read_text(encoding="utf-8")
    return send_message(receiver, message)


if __name__ == "__main__":
    raise SystemExit(main())
