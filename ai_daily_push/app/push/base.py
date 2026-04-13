from __future__ import annotations

from abc import ABC, abstractmethod


class MessageSender(ABC):
    @abstractmethod
    def send_text(self, message: str) -> str:
        raise NotImplementedError
