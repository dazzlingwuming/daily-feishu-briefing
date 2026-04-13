[中文](./GITHUB_PUBLISHING.zh-CN.md) | English

# GitHub Publishing Guide

This file is for maintainers of this repository.

## Safe To Commit

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

## Before A Public Push

1. Confirm `.env` is not tracked.
2. Confirm no real credentials or receiver IDs appear in examples.
3. Confirm generated files and logs are ignored.
4. Confirm runtime artifacts are not staged.
