[English](./GITHUB_PUBLISHING.md) | 中文

# GitHub 发布说明

这个文件说明哪些内容适合上传，哪些内容应该只保留在本地。

## 建议上传这些内容

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

## 这些内容只保留在本地

- `ai_daily_push/.env`
- 任何真实 `FEISHU_RECEIVER_OPEN_ID`
- 任何真实 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- 所有 `*.db`
- 所有生成出来的日报文本
- 所有调度日志
- 本地 IDE 文件

## 建议在仓库 README 里说明

如果你准备公开发布，建议在 README 里明确写清：

1. 这个项目支持两种模式：独立 Python 模式和 Codex 定时调度模式。
2. 飞书发送依赖本地 `lark-cli` 或 API 凭证。
3. Codex 调度器只适合运行在你自己可信的机器上。
4. 仓库示例里只应使用占位值，不要放真实配置。

## 建议第一次公开提交包含

- 源代码
- 脚本
- 测试
- 文档
- `.env.example`
- `.gitignore`

第一次公开提交不要包含任何运行时生成产物。
