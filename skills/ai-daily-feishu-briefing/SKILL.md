---
name: ai-daily-feishu-briefing
description: Create, extend, debug, or operate a daily AI papers and AI news briefing workflow that collects sources, deduplicates items, generates structured Chinese summaries, and pushes the result to Feishu private chat.
---

# AI Daily Feishu Briefing

Use this skill when Codex itself should gather AI papers and AI news, summarize them into a readable Chinese daily briefing, and deliver the result to Feishu private chat.

This skill has two modes, in this order of priority:

1. `Codex-driven briefing mode`
2. `Project-building mode`

Default to mode 1 unless the user explicitly asks for a standalone project, service, scheduler, or codebase changes.

## Workflow

When the user asks for a daily briefing, follow this order unless the request is narrower:

1. Decide whether this is:
   a. a direct briefing request
   b. a project-building request
2. For direct briefing requests, do not default into project scaffolding.
3. Verify or infer the active send mode:
   - `cli` for local environments with working `lark-cli`
   - `api` for server or CI environments using `app_id` and `app_secret`
4. Gather candidate items from the default sources or the sources explicitly requested by the user.
5. Remove duplicates and keep only the highest-signal items.
6. Write the final briefing in Chinese in the expected concise format.
7. Send the result to Feishu.
8. Only move into project-building mode if the user explicitly asks for persistent automation or code changes.

## Codex-Driven Briefing Mode

Use this mode for prompts like:

- 每天帮我推送 AI 论文和资讯到飞书
- 现在帮我整理今天的 AI 日报并发给我
- 抓最新热点，整理成日报，通过飞书私聊发我

In this mode:

- Codex should gather sources directly using available tools or existing scripts
- Codex should summarize and format the content directly
- Codex should optimize for readability, not raw completeness

Use this output structure by default:

```text
AI 每日速递
今天共 X 篇论文，Y 条资讯。

【今日论文】
1. 标题
一句话摘要：这篇论文解决了什么问题，方法上有什么新东西。
关键点：亮点1；亮点2
为什么值得关注：这对谁有价值，适合什么方向的人看
链接：https://...

【今日资讯】
1. 标题
一句话摘要：发生了什么事
关键点：发布了什么；影响了谁
为什么值得关注：对产品、研发或业务判断意味着什么
链接：https://...
```

Prefer fewer items with stronger summaries over more items with generic text.

Read [references/codex-workflow.md](references/codex-workflow.md) for the direct briefing workflow and summary rules.

## Delivery Modes

There are two valid delivery modes.

### Mode 1: CLI Send

Prefer this for local development when `lark-cli` already works.

On Windows, prefer this path when Codex is running inside `pwsh` / PowerShell 7 (`PSEdition = Core`).
When Codex is running from legacy `powershell.exe` / Windows PowerShell 5 (`PSEdition = Desktop`), prefer writing the final report to a UTF-8 file and letting a Python helper send that file instead of inlining a long Chinese payload through the old shell.

Typical pattern:

```powershell
lark-cli im +messages-send --as bot --user-id "ou_xxx" --text "..."
```

### Mode 2: API Send

Prefer this for production or headless execution.

Required flow:

1. Get tenant access token from `FEISHU_APP_ID` and `FEISHU_APP_SECRET`
2. Send text message to `FEISHU_RECEIVER_OPEN_ID`
3. Record status and message ID

Read [references/feishu.md](references/feishu.md) when implementing or debugging Feishu delivery.

## Project-Building Mode

Only use this mode when the user explicitly wants a persistent project or automation setup.

Typical triggers:

- 给我建一个每天自动跑的项目
- 做一个 Python 服务来定时推送
- 把这个流程做成代码和定时任务

## Recommended Project Shape

Use this structure by default unless the repo already has a stronger convention:

```text
app/
  models.py
  config.py
  logger.py
  main.py
  sources/
  pipeline/
  push/
  storage/
scripts/
tests/
```

## Summary Generation

Always generate structured JSON, not free-form prose.

Use the prompt and fallback rules in [references/prompting.md](references/prompting.md).

Requirements:

- Produce valid JSON
- Avoid empty language
- Avoid literal translation when summarizing English sources
- Preserve enough detail to explain why the item matters

If summarization fails for an item, degrade to the title plus a trimmed source summary instead of failing the whole report.

## Validation

Minimum acceptable validation for this skill's output:

1. A source fetch returns items.
2. Dedup and selection run without crashing.
3. Summary generation returns parseable JSON.
4. Report rendering produces readable text.
5. A Feishu test message reaches the configured recipient.
6. Push history prevents duplicate sends on rerun.

If helper scripts exist, prefer using them:

- `scripts/doctor.py`
- `scripts/send_test_message.py`
