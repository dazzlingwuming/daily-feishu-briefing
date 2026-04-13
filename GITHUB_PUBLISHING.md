[中文](./GITHUB_PUBLISHING.zh-CN.md) | English

# GitHub Publishing Guide

This file describes what should be uploaded and what should remain local.

## Upload These

- `skills/ai-daily-feishu-briefing/`
- `ai_daily_push/app/`
- `ai_daily_push/scripts/`
- `ai_daily_push/tests/`
- `ai_daily_push/.env.example`
- `ai_daily_push/requirements.txt`
- `ai_daily_push/README.md`
- `ai_daily_push/README.zh-CN.md`
- `codex_scheduler/*.ps1`
- `codex_scheduler/briefing_prompt.txt`
- `codex_scheduler/README.md`
- `codex_scheduler/README.zh-CN.md`
- root `README.md`
- root `README.zh-CN.md`
- root `.gitignore`

## Keep Local Only

- `ai_daily_push/.env`
- any real `FEISHU_RECEIVER_OPEN_ID`
- any real `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- all `*.db`
- all generated briefing text files
- all scheduler logs
- local IDE files

## Suggested Repo README Notes

If you publish this publicly, explain:

1. The project supports two modes: standalone Python mode and Codex-driven scheduled mode.
2. Feishu delivery requires local `lark-cli` or API credentials.
3. The Codex scheduler is intended for a trusted personal machine.
4. The included examples use placeholder values only.

## Suggested First Commit Contents

- source code
- scripts
- tests
- docs
- `.env.example`
- `.gitignore`

Do not include any generated runtime output in the first public commit.
