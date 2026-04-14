# Codex Workflow

## Primary Intent

This skill is primarily for a live Codex session that should:

1. gather today's AI papers and AI news
2. select the most relevant items
3. summarize them in Chinese
4. send the result to Feishu

Do not default into building a standalone service unless the user explicitly asks for code or automation.

## Direct Briefing Workflow

### Step 1: Gather

Use the highest-signal sources first:

- arXiv: `cs.AI`, `cs.LG`, `cs.CL`, `stat.ML`
- OpenAI Blog
- Anthropic News
- DeepMind Blog
- Hugging Face Blog

Prefer official sources and recent items.

### Step 2: Select

Default target:

- 3 papers
- 3 news items

If source quality is weak, send fewer items rather than padding with low-signal content.

### Step 3: Summarize

For each paper:

- `一句话摘要` should state the problem and what is new in the method or framing
- `关键点` should capture 1-2 concrete highlights, not generic praise
- `为什么值得关注` should say who should care and in what context

For each news item:

- `一句话摘要` should state what happened
- `关键点` should say what was released or changed and who it affects
- `为什么值得关注` should connect it to product, engineering, or business judgment

## Anti-Patterns

Avoid lines like:

- “这是近期值得跟踪的 AI 内容”
- “适合作为动态输入”
- “值得关注”

unless they are followed by a concrete reason.

Bad:

```text
为什么值得关注：这是近期值得跟踪的 AI 内容。
```

Good:

```text
为什么值得关注：如果你在评估企业内部 AI 落地，这条内容能帮助你判断 OpenAI 正在把能力重点放在哪些协作和交付场景。
```

## Desired Output Style

Write for fast scanning.

- Keep each field short
- Prefer concrete nouns and verbs
- Avoid repeating the same why-it-matters sentence across different items
- Prefer differentiation over uniformity

## Feishu Sending

After the briefing is complete, send it through the configured Feishu path.

If the message is multiline, prefer a structured `post` payload over plain `text`.

On Windows, prefer this decision rule:

- if running in `pwsh` / PowerShell 7, Codex can send directly with `lark-cli`
- if running in legacy `powershell.exe`, prefer writing the report to a UTF-8 file and letting a Python helper send it
