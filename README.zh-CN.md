[English](./README.md) | 中文

# 每日飞书简报

这个仓库提供一套可复用的“日报生成并发送到飞书私聊”的工作流。

它支持两种使用方式：

- `Codex + skill 模式`
  由 Codex 使用 `ai-daily-feishu-briefing` skill 抓取信息源、筛选重点、撰写中文日报。调度层会先落一份 UTF-8 日报文件，然后自动按 shell 环境选择发送方式：
  `pwsh/Core` 走 Codex 直发，旧 `powershell.exe/Desktop` 回退到 Python sender。
- `独立 Python 模式`
  由 `ai_daily_push` 项目在运行时独立完成抓取、排序、渲染和发送。

## 仓库结构

- `skills/ai-daily-feishu-briefing/`
  仓库内保存的 Codex skill 源码
- `ai_daily_push/`
  负责抓取、排序、渲染和发送的独立 Python 项目
- `codex_scheduler/`
  用来通过 `codex exec` 运行 skill、生成日报文件并发送到飞书、同时接入 Windows 任务计划程序的包装脚本

## 快速开始

### 方案一：使用 Codex Skill

1. 先把 skill 安装到本机的 Codex skills 目录：

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<你的用户名>\.codex\skills\ai-daily-feishu-briefing
```

2. 重新打开一个新的 Codex 会话。

3. 用类似下面的提示词触发：

```text
Use $ai-daily-feishu-briefing，抓取今天最重要的 AI 论文和 AI 资讯，整理成中文日报，并发送到我的飞书私聊。
```

完整 skill 使用说明见：

- [skills/ai-daily-feishu-briefing/README.md](./skills/ai-daily-feishu-briefing/README.md)
- [skills/ai-daily-feishu-briefing/README.zh-CN.md](./skills/ai-daily-feishu-briefing/README.zh-CN.md)

### 方案二：使用 Python 项目

```powershell
cd ai_daily_push
python scripts\init_db.py
python scripts\send_test_message.py --message "smoke test"
python scripts\run_once.py --ignore-history
```

详细说明见：

- [ai_daily_push/README.md](./ai_daily_push/README.md)
- [ai_daily_push/README.zh-CN.md](./ai_daily_push/README.zh-CN.md)

## Codex 调度器

先判断你当前开的终端是哪一种 PowerShell：

```powershell
$PSVersionTable.PSEdition
```

结果含义：

- `Core`：你当前就在 `pwsh` / PowerShell 7 里，推荐直接走 Codex 直发链路
- `Desktop`：你当前在旧 `powershell.exe` / Windows PowerShell 5 里，会自动回退到 Python sender

如果你想进入 `pwsh`，直接执行：

```powershell
pwsh
```

如果你想跑 Codex 驱动的执行链路，可以直接运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

如果你想优先使用“Codex 直发飞书”链路，建议从 `pwsh` / PowerShell 7 运行：

```powershell
pwsh -File .\codex_scheduler\run_codex_briefing.ps1
```

如果你想安装成 Windows 每日任务：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "08:30"
```

以后如果不要了：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

查看下一次执行时间：

```powershell
(Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing").NextRunTime
```

查看当前任务状态：

```powershell
Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing" | Select-Object LastRunTime,LastTaskResult,NextRunTime
```

详细说明见：

- [codex_scheduler/README.md](./codex_scheduler/README.md)
- [codex_scheduler/README.zh-CN.md](./codex_scheduler/README.zh-CN.md)

## 说明

- 飞书发送依赖本地 `lark-cli` 或飞书 API 凭证。
- Codex 调度模式更适合运行在你自己可信的个人机器上。
- Windows 下推荐优先使用 `pwsh` / PowerShell 7，这样 Codex 可以直接稳定发送中文。
- 如果使用者仍在旧 `powershell.exe` / Windows PowerShell 5 里运行，仓库会自动回退到 UTF-8 文件 + Python sender 的兼容路径。
- 这份 skill 文档里也说明了：如果以后想扩展成商业、金融、政策等主题，应该优先改哪些文件。

如果你是维护仓库、准备发布或检查哪些文件适合上传，请看：

- [GITHUB_PUBLISHING.md](./GITHUB_PUBLISHING.md)
- [GITHUB_PUBLISHING.zh-CN.md](./GITHUB_PUBLISHING.zh-CN.md)
