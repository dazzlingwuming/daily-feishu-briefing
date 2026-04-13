[English](./README.md) | 中文

# Codex 调度层

这个目录保存的是 Codex 驱动的包装层。

它主要做四件事：

1. 调用 `codex exec`
2. 使用本地安装的 `ai-daily-feishu-briefing` skill
3. 把最终中文日报写入 UTF-8 文本文件
4. 再通过 `ai_daily_push` 里的稳定飞书发送器把这个文件发出去

这样设计的目的，是避免把很长的中文正文直接内联进 shell 命令。在 Windows 上，这种方式明显更稳定。

## 文件说明

- `briefing_prompt.txt`
  传给 Codex 的非交互 prompt
- `run_codex_briefing.ps1`
  主包装脚本
- `install_codex_briefing_task.ps1`
  安装每日 Windows 计划任务
- `uninstall_codex_briefing_task.ps1`
  删除该计划任务

## 手动执行一次

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

## 安装每日任务

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "09:00"
```

## 删除每日任务

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

## 成功时会看到什么

成功时通常会出现：

- 新的 `ai_daily_push/briefing_feishu_today.txt`
- `codex_scheduler/logs/` 下的新日志
- 控制台打印的飞书消息 ID
- 最后一行成功提示：
  `Report generated and Feishu delivery completed.`

## 使用前提

这套流程使用：

```text
codex exec --search --dangerously-bypass-approvals-and-sandbox
```

只建议运行在你自己可控、可信的机器和工作区里。
