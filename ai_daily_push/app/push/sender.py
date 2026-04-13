from __future__ import annotations

from app.config import Settings
from app.push.base import MessageSender
from app.push.feishu_api_sender import FeishuApiSender
from app.push.feishu_cli_sender import FeishuCliSender


def build_sender(settings: Settings) -> MessageSender:
    if settings.feishu_send_mode == "api":
        return FeishuApiSender(settings)
    return FeishuCliSender(settings)
