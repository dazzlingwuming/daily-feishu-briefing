from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


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
    if path:
        env.update(read_env_file(path))
    return env


def resolve_message(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    return args.message


def send_via_cli(env: dict[str, str], message: str) -> int:
    receiver = env.get("FEISHU_RECEIVER_OPEN_ID", "").strip()
    if not receiver:
        raise SystemExit("FEISHU_RECEIVER_OPEN_ID is required")

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
        "--text",
        message,
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def fetch_token(env: dict[str, str]) -> str:
    app_id = env.get("FEISHU_APP_ID", "").strip()
    app_secret = env.get("FEISHU_APP_SECRET", "").strip()
    if not app_id or not app_secret:
        raise SystemExit("FEISHU_APP_ID and FEISHU_APP_SECRET are required for api mode")

    body = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    token = payload.get("tenant_access_token")
    if not token:
        raise SystemExit(f"failed to get token: {payload}")
    return token


def send_via_api(env: dict[str, str], message: str) -> int:
    receiver = env.get("FEISHU_RECEIVER_OPEN_ID", "").strip()
    if not receiver:
        raise SystemExit("FEISHU_RECEIVER_OPEN_ID is required")

    token = fetch_token(env)
    payload = {
        "receive_id": receiver,
        "msg_type": "text",
        "content": json.dumps({"text": message}, ensure_ascii=False),
    }
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(resp.read().decode("utf-8"))
        return 0
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"), file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a Feishu smoke-test message using cli or api mode.")
    parser.add_argument("--env-file", default=".env", help="Path to a dotenv-style file")
    parser.add_argument("--mode", choices=["cli", "api"], help="Override FEISHU_SEND_MODE")
    parser.add_argument("--message", default="AI Daily Briefing smoke test", help="Message text")
    parser.add_argument("--file", help="Read message content from a UTF-8 text file")
    args = parser.parse_args()

    env = load_env(Path(args.env_file))
    mode = (args.mode or env.get("FEISHU_SEND_MODE", "cli")).strip().lower() or "cli"
    message = resolve_message(args)
    if mode == "cli":
        return send_via_cli(env, message)
    if mode == "api":
        return send_via_api(env, message)
    raise SystemExit(f"unsupported mode: {mode}")


if __name__ == "__main__":
    raise SystemExit(main())
