from __future__ import annotations

import json
import re
import urllib.request

from app.config import Settings
from app.models import ContentItem, SummaryResult


def _clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def _first_sentence(text: str, limit: int = 160) -> str:
    text = _clean_text(text)
    if not text:
        return ""
    parts = re.split(r"(?<=[\.\!\?。；;])\s+", text)
    sentence = parts[0] if parts else text
    return sentence[:limit].rstrip(" ,;，；")


def _keyword_flags(text: str) -> list[str]:
    haystack = text.lower()
    mapping = [
        ("agent", "和 Agent/智能体相关"),
        ("reason", "涉及推理能力"),
        ("multimodal", "涉及多模态"),
        ("video", "和视频生成/理解相关"),
        ("audio", "和音频生成/理解相关"),
        ("benchmark", "包含评测或基准信号"),
        ("enterprise", "偏企业落地"),
        ("api", "和 API/开发者能力相关"),
        ("open source", "涉及开源能力"),
        ("security", "和安全事件或风险相关"),
        ("release", "属于发布/更新类信息"),
    ]
    results: list[str] = []
    for needle, label in mapping:
        if needle in haystack:
            results.append(label)
    return results[:2]


def _paper_fallback(item: ContentItem) -> SummaryResult:
    summary_text = _clean_text(item.summary)
    sentence = _first_sentence(summary_text) or f"这篇论文围绕《{item.title}》提出了新的方法或分析框架。"
    highlights = _keyword_flags(f"{item.title} {summary_text}")
    if not highlights:
        highlights = [
            "关注方法设计与实验结果",
            "适合继续查看原文中的任务设置与评测细节",
        ]
    why = "适合关注模型能力、评测结果、Agent、多模态或应用方向的人快速判断是否值得精读。"
    return SummaryResult(
        brief=sentence,
        highlights=highlights,
        why_it_matters=why,
    )


def _news_fallback(item: ContentItem) -> SummaryResult:
    summary_text = _clean_text(item.summary)
    sentence = _first_sentence(summary_text) or f"这条资讯和《{item.title}》相关，重点是最新发布、变更或官方说明。"
    highlights = _keyword_flags(f"{item.title} {summary_text}")
    if "openai_blog" in item.source:
        highlights.insert(0, "来自 OpenAI 官方渠道")
    elif "anthropic" in item.source:
        highlights.insert(0, "来自 Anthropic 官方渠道")
    elif "deepmind" in item.source:
        highlights.insert(0, "来自 DeepMind 官方渠道")
    elif "huggingface" in item.source:
        highlights.insert(0, "来自 Hugging Face 官方渠道")
    deduped: list[str] = []
    for value in highlights:
        if value not in deduped:
            deduped.append(value)
    highlights = deduped[:2] or ["偏官方动态", "适合快速判断是否需要跟进"]
    why = "适合产品、研发和业务侧快速判断这条官方动态是否会影响功能规划、技术选型或行业判断。"
    return SummaryResult(
        brief=sentence,
        highlights=highlights,
        why_it_matters=why,
    )


def _fallback_summary(item: ContentItem) -> SummaryResult:
    if item.item_type == "paper":
        return _paper_fallback(item)
    return _news_fallback(item)


def summarize_item(item: ContentItem, settings: Settings) -> SummaryResult:
    if not settings.openai_api_key:
        return _fallback_summary(item)

    prompt = (
        "你是一个 AI 行业研究编辑。请根据输入内容输出中文 JSON，"
        "包含 brief, highlights, why_it_matters 三个字段。"
    )
    body = {
        "model": settings.openai_model,
        "input": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"标题: {item.title}\n摘要: {item.summary}\n来源: {item.source}\n类型: {item.item_type}",
            },
        ],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.openai_api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        text = payload["output"][0]["content"][0]["text"]
        parsed = json.loads(text)
        return SummaryResult(
            brief=parsed["brief"],
            highlights=list(parsed["highlights"]),
            why_it_matters=parsed["why_it_matters"],
        )
    except Exception:
        return _fallback_summary(item)
