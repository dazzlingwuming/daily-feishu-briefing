[English](./GITHUB_PUBLISHING.md) | 中文

# GitHub 发布说明

这个文件是写给仓库维护者看的。

## 可以提交到仓库的内容

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
- 根目录 `README.md`
- 根目录 `README.zh-CN.md`
- 根目录 `.gitignore`

## 只保留在本地的内容

- `ai_daily_push/.env`
- 任何真实 `FEISHU_RECEIVER_OPEN_ID`
- 任何真实 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- 所有 `*.db`
- 所有生成出来的日报文本
- 所有调度日志
- 本地 IDE 文件

## 公开推送前检查

1. 确认 `.env` 没有被跟踪。
2. 确认示例里没有真实凭证或接收人 ID。
3. 确认生成文件和日志都被忽略。
4. 确认运行时产物没有被暂存。
