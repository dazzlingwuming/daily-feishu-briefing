# Prompting

## Required Output Format

Always request valid JSON:

```json
{
  "brief": "2句话概括核心内容",
  "highlights": ["关键点1", "关键点2"],
  "why_it_matters": "为什么值得关注"
}
```

## Baseline Prompt

```text
你是一个 AI 行业研究编辑。请根据输入内容输出中文 JSON：
{
  "brief": "2句话概括核心内容",
  "highlights": ["2个关键点"],
  "why_it_matters": "这条内容为什么值得产品经理、工程负责人和 AI 应用创业者关注"
}

要求：
1. 不要空话
2. 不要逐字直译
3. 优先写信息增量
4. 输出必须是合法 JSON
```

## Paper Prompt Notes

- Use title plus abstract as the minimum input.
- Emphasize method novelty, benchmark relevance, and practical implications.
- Avoid overstating impact when the source is only an arXiv preprint.

## News Prompt Notes

- Use title plus the most informative body excerpt or summary.
- Emphasize what changed, who it affects, and why it matters now.
- Prefer concrete product or ecosystem impact over generic commentary.

## Fallback Rules

If parsing fails:

1. Retry once with a stricter `valid JSON only` instruction.
2. If it still fails, degrade to:
   - original title
   - trimmed source summary
   - a short generated `why_it_matters` line if possible

If content is sparse:

- Admit uncertainty
- Keep `brief` short
- Do not invent details
