[中文](./README.zh-CN.md) | English

# Codex Scheduler

This folder contains the Codex-driven wrapper around the briefing workflow.

It does four things:

1. calls `codex exec`
2. uses the local `ai-daily-feishu-briefing` skill
3. writes the final Chinese briefing into a UTF-8 text file
4. sends that file through the stable Feishu sender in `ai_daily_push`

This design avoids passing large Chinese payloads inline through shell command strings, which is less stable on Windows.

## Files

- `briefing_prompt.txt`
  The non-interactive prompt passed to Codex
- `run_codex_briefing.ps1`
  Main wrapper script
- `install_codex_briefing_task.ps1`
  Register a daily Windows scheduled task
- `uninstall_codex_briefing_task.ps1`
  Remove the scheduled task

## Run Once

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

## Install Daily Task

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "09:00"
```

## Remove Daily Task

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

## Expected Success Signals

When the wrapper succeeds, you should see:

- a new `ai_daily_push/briefing_feishu_today.txt`
- a new file under `codex_scheduler/logs/`
- a Feishu message ID in the console
- a final success line:
  `Report generated and Feishu delivery completed.`

## Trust Model

This workflow uses:

```text
codex exec --search --dangerously-bypass-approvals-and-sandbox
```

Use it only on a machine and workspace you control.
