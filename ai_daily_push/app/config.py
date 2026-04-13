from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _read_env_file(path: Path) -> dict[str, str]:
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


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or (PROJECT_ROOT / ".env")
    for key, value in _read_env_file(env_path).items():
        os.environ.setdefault(key, value)


def _flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    app_env: str
    openai_api_key: str
    openai_model: str
    feishu_send_mode: str
    feishu_app_id: str
    feishu_app_secret: str
    feishu_receiver_open_id: str
    paper_top_k: int
    news_top_k: int
    push_schedule: str
    enable_openai_blog: bool
    enable_anthropic_blog: bool
    enable_deepmind_blog: bool
    enable_hf_blog: bool
    database_path: Path
    arxiv_contact_email: str


def get_settings() -> Settings:
    load_dotenv()
    database_value = os.getenv("DATABASE_PATH", "")
    database_path = Path(database_value) if database_value else PROJECT_ROOT / "data.db"
    return Settings(
        app_env=os.getenv("APP_ENV", "dev"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        feishu_send_mode=os.getenv("FEISHU_SEND_MODE", "cli").strip().lower(),
        feishu_app_id=os.getenv("FEISHU_APP_ID", ""),
        feishu_app_secret=os.getenv("FEISHU_APP_SECRET", ""),
        feishu_receiver_open_id=os.getenv("FEISHU_RECEIVER_OPEN_ID", ""),
        paper_top_k=int(os.getenv("PAPER_TOP_K", "3")),
        news_top_k=int(os.getenv("NEWS_TOP_K", "3")),
        push_schedule=os.getenv("PUSH_SCHEDULE", "09:00"),
        enable_openai_blog=_flag("ENABLE_OPENAI_BLOG", True),
        enable_anthropic_blog=_flag("ENABLE_ANTHROPIC_BLOG", True),
        enable_deepmind_blog=_flag("ENABLE_DEEPMIND_BLOG", True),
        enable_hf_blog=_flag("ENABLE_HF_BLOG", True),
        database_path=database_path,
        arxiv_contact_email=os.getenv("ARXIV_CONTACT_EMAIL", ""),
    )
