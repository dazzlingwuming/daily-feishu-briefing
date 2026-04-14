[中文](./README.zh-CN.md) | English

# Codex Scheduler

This folder contains the Codex-driven wrapper around the briefing workflow.

It does four things:

1. calls `codex exec`
2. uses the local `ai-daily-feishu-briefing` skill
3. writes the final Chinese briefing into a UTF-8 text file
4. chooses a delivery path based on the active shell:
   direct Codex delivery on `pwsh/Core`, Python fallback sender on `powershell.exe/Desktop`

This design keeps direct delivery available on modern PowerShell while preserving a safer UTF-8 file fallback for legacy Windows PowerShell.

## Files

- `briefing_prompt.txt`
  The non-interactive prompt passed to Codex
- `run_codex_briefing.ps1`
  Main wrapper script; detects `Core` vs `Desktop`
- `send_feishu_from_file.py`
  Python fallback sender for legacy Windows PowerShell
- `install_codex_briefing_task.ps1`
  Register a daily Windows scheduled task
- `uninstall_codex_briefing_task.ps1`
  Remove the scheduled task

## Run Once

First, check which shell you are in:

```powershell
$PSVersionTable.PSEdition
```

Meaning:

- `Core`: current shell is `pwsh` / PowerShell 7, so direct Codex delivery is preferred
- `Desktop`: current shell is legacy `powershell.exe` / Windows PowerShell 5, so the wrapper will fall back to the Python sender

If you are not in `pwsh` yet, start it with:

```powershell
pwsh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

To prefer the direct Codex delivery path, run it from `pwsh` / PowerShell 7:

```powershell
pwsh -File .\codex_scheduler\run_codex_briefing.ps1
```

## Install Daily Task

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "09:00"
```

## Check Task Status

See the full task info:

```powershell
Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing"
```

Show only the most useful fields:

```powershell
Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing" | Select-Object LastRunTime,LastTaskResult,NextRunTime
```

Show only the next run time:

```powershell
(Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing").NextRunTime
```

## Trigger It Manually

```powershell
Start-ScheduledTask -TaskName "Codex AI Daily Briefing"
```

## Remove Daily Task

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

## Expected Success Signals

When the wrapper succeeds, you should see:

- a new `codex_scheduler/output/briefing_feishu_today.txt`
- a new file under `codex_scheduler/logs/`
- a Feishu message ID in the console
- a final success line:
  - `Report generated and Codex direct Feishu delivery completed.`
  - or `Report generated and Feishu delivery completed via Python fallback sender.`

If the task is still running, `LastTaskResult` may temporarily show `267009`, which means the scheduled task is currently running.

## Trust Model

This workflow uses:

```text
codex exec --search --dangerously-bypass-approvals-and-sandbox
```

Use it only on a machine and workspace you control.
