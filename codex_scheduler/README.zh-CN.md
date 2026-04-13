[English](./README.md) | 中文

# Codex 调度层

这个目录负责 Codex 驱动的日报流程：

1. 调用 `codex exec`
2. 使用本地安装的 `ai-daily-feishu-briefing` skill
3. 把最终中文日报生成到一个 UTF-8 文件
4. 再通过 `ai_daily_push` 里的稳定飞书发送器发送该文件

这套设计是有意为之的。这样可以避免把很长的中文正文直接内联进 shell 命令，在 Windows 上会更稳定。

## 文件说明

- `briefing_prompt.txt`
  给包装脚本使用的非交互 Codex prompt
- `run_codex_briefing.ps1`
  主包装脚本
- `install_codex_briefing_task.ps1`
  注册每天自动执行的 Windows 计划任务
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

## 成功时你会看到什么

当包装脚本成功时，通常会出现：

- 新的 `ai_daily_push/briefing_feishu_today.txt`
- `codex_scheduler/logs/` 下出现新日志
- 控制台打印一个飞书消息 ID
- 最后一行提示：
  `Report generated and Feishu delivery completed.`

## 信任边界说明

这套流程使用：

```text
codex exec --search --dangerously-bypass-approvals-and-sandbox
```

只建议在你自己控制的机器和工作区里使用。
