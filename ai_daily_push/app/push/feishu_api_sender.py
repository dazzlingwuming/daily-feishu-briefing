from __future__ import annotations

import json
import urllib.request

from app.config import Settings
from app.push.base import MessageSender


class FeishuApiSender(MessageSender):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _token(self) -> str:
        body = json.dumps(
            {"app_id": self.settings.feishu_app_id, "app_secret": self.settings.feishu_app_secret}
        ).encode("utf-8")
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        token = payload.get("tenant_access_token")
        if not token:
            raise RuntimeError(f"failed to fetch token: {payload}")
        return token

    def send_text(self, message: str) -> str:
        token = self._token()
        payload = {
            "receive_id": self.settings.feishu_receiver_open_id,
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
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result.get("data", {}).get("message_id", "")
