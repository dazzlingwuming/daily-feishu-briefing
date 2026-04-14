[English](./README.md) | 中文

# Codex 调度层

这个目录保存的是 Codex 驱动的包装层。

它主要做四件事：

1. 调用 `codex exec`
2. 使用本地安装的 `ai-daily-feishu-briefing` skill
3. 把最终中文日报写入 UTF-8 文本文件
4. 根据当前 shell 自动选择发送方式：
   `pwsh/Core` 让 Codex 直发，`powershell.exe/Desktop` 回退到 Python sender

这样设计的目的，是兼顾两种 Windows 环境：

- 在 `pwsh` / PowerShell 7 里，Codex 可以直接用 `lark-cli` 发中文
- 在旧 `powershell.exe` 里，仍然保留 UTF-8 文件 + Python sender 的稳妥路径

## 文件说明

- `briefing_prompt.txt`
  传给 Codex 的非交互 prompt
- `run_codex_briefing.ps1`
  主包装脚本，会自动判断当前是 `Core` 还是 `Desktop`
- `send_feishu_from_file.py`
  旧 PowerShell 下的回退 sender，读取 UTF-8 文件并通过 `lark-cli` 发送
- `install_codex_briefing_task.ps1`
  安装每日 Windows 计划任务
- `uninstall_codex_briefing_task.ps1`
  删除该计划任务

## 手动执行一次

先判断你当前在哪个 shell：

```powershell
$PSVersionTable.PSEdition
```

结果含义：

- `Core`：当前是 `pwsh` / PowerShell 7，推荐让 Codex 直发
- `Desktop`：当前是旧 `powershell.exe` / Windows PowerShell 5，会自动回退到 Python sender

如果你当前还没进入 `pwsh`，可以先执行：

```powershell
pwsh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

如果你希望优先走“Codex 直发”链路，建议在 `pwsh` / PowerShell 7 里运行：

```powershell
pwsh -File .\codex_scheduler\run_codex_briefing.ps1
```

## 安装每日任务

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "09:00"
```

## 查看任务状态

查看完整状态：

```powershell
Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing"
```

只看最常用的几个字段：

```powershell
Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing" | Select-Object LastRunTime,LastTaskResult,NextRunTime
```

只看下一次执行时间：

```powershell
(Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing").NextRunTime
```

## 手动触发一次

```powershell
Start-ScheduledTask -TaskName "Codex AI Daily Briefing"
```

## 删除每日任务

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

## 成功时会看到什么

成功时通常会出现：

- 新的 `codex_scheduler/output/briefing_feishu_today.txt`
- `codex_scheduler/logs/` 下的新日志
- 控制台打印的飞书消息 ID
- 最后一行成功提示：
  - `Report generated and Codex direct Feishu delivery completed.`
  - 或 `Report generated and Feishu delivery completed via Python fallback sender.`

如果任务还在运行中，`LastTaskResult` 可能会暂时显示 `267009`，这表示计划任务当前仍在执行。

## 使用前提

这套流程使用：

```text
codex exec --search --dangerously-bypass-approvals-and-sandbox
```

只建议运行在你自己可控、可信的机器和工作区里。
