from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.models import ContentItem


class SourceAdapter(ABC):
    name: str

    @abstractmethod
    def fetch(self) -> List[ContentItem]:
        raise NotImplementedError
