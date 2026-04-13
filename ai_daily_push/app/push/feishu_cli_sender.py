from __future__ import annotations

import json
import shutil
import subprocess

from app.config import Settings
from app.push.base import MessageSender


class FeishuCliSender(MessageSender):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def send_text(self, message: str) -> str:
        cli = shutil.which("lark-cli") or shutil.which("lark-cli.cmd") or shutil.which("lark-cli.CMD")
        if not cli:
            raise RuntimeError("lark-cli not found in PATH")
        if not self.settings.feishu_receiver_open_id:
            raise RuntimeError("FEISHU_RECEIVER_OPEN_ID is required")

        cmd = [
            cli,
            "im",
            "+messages-send",
            "--as",
            "bot",
            "--user-id",
            self.settings.feishu_receiver_open_id,
        ]

        if "\n" in message:
            lines = [line.rstrip() for line in message.splitlines()]
            title = next((line for line in lines if line.strip()), "AI 每日速递")
            content = []
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
            payload = {
                "zh_cn": {
                    "title": title,
                    "content": content or [[{"tag": "text", "text": title}]],
                }
            }
            cmd.extend(["--msg-type", "post", "--content", json.dumps(payload, ensure_ascii=False)])
        else:
            cmd.extend(["--text", message])

        result = subprocess.run(cmd, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "lark-cli send failed")
        payload = json.loads(result.stdout)
        return payload.get("data", {}).get("message_id", "")
