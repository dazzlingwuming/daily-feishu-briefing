from __future__ import annotations

from typing import Iterable

from app.models import BriefingItem


def _render_item(idx: int, item: BriefingItem) -> list[str]:
    highlights = "；".join(item.summary.highlights)
    return [
        f"{idx}. {item.content.title}",
        f"一句话摘要：{item.summary.brief}",
        f"关键点：{highlights}",
        f"为什么值得关注：{item.summary.why_it_matters}",
        f"链接：{item.content.url}",
    ]


def render_section(title: str, items: Iterable[BriefingItem]) -> list[str]:
    materialized = list(items)
    lines = [title]
    if not materialized:
        lines.extend(["今日无新增内容。", ""])
        return lines

    for idx, item in enumerate(materialized, start=1):
        lines.extend(_render_item(idx, item))
        lines.append("")
    return lines


def render_daily_report(papers: list[BriefingItem], news: list[BriefingItem]) -> str:
    lines = [
        "AI 每日速递",
        f"今天共 {len(papers)} 篇论文，{len(news)} 条资讯。",
        "",
    ]
    lines.extend(render_section("【今日论文】", papers))
    lines.extend(render_section("【今日资讯】", news))
    report = "\n".join(lines).strip()
    return report.replace("\u2011", "-")
