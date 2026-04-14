[中文](./README.zh-CN.md) | English

# Daily Feishu Briefing

This repository provides a reusable workflow for generating a daily briefing and sending it to Feishu private chat.

It supports two usage modes:

- `Codex + skill mode`
  Codex uses the `ai-daily-feishu-briefing` skill to gather sources, select the strongest items, write the final Chinese briefing, and send it through the stable Feishu sender.
- `Standalone Python mode`
  The `ai_daily_push` project fetches, ranks, renders, and sends the briefing without depending on Codex at runtime.

## Repository Structure

- `skills/ai-daily-feishu-briefing/`
  Repository copy of the Codex skill source
- `ai_daily_push/`
  Standalone Python project for fetching, ranking, rendering, and sending
- `codex_scheduler/`
  Wrapper scripts for running the skill through `codex exec` and Windows Task Scheduler

## Quick Start

### Option 1: Use The Codex Skill

1. Install the skill into your local Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<YourUser>\.codex\skills\ai-daily-feishu-briefing
```

2. Start a new Codex session.

3. Trigger it with a prompt such as:

```text
Use $ai-daily-feishu-briefing to gather today's most important AI papers and AI news, summarize them in Chinese, and send the final briefing to my Feishu private chat.
```

See the full skill guide:

- [skills/ai-daily-feishu-briefing/README.md](./skills/ai-daily-feishu-briefing/README.md)
- [skills/ai-daily-feishu-briefing/README.zh-CN.md](./skills/ai-daily-feishu-briefing/README.zh-CN.md)

### Option 2: Use The Python Project

```powershell
cd ai_daily_push
python scripts\init_db.py
python scripts\send_test_message.py --message "smoke test"
python scripts\run_once.py --ignore-history
```

See:

- [ai_daily_push/README.md](./ai_daily_push/README.md)
- [ai_daily_push/README.zh-CN.md](./ai_daily_push/README.zh-CN.md)

## Codex Scheduler

If you want a Codex-driven scheduled run, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

Install a daily Windows task:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "08:30"
```

Remove it later:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

Check the next run time:

```powershell
(Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing").NextRunTime
```

Check the current task status:

```powershell
Get-ScheduledTaskInfo -TaskName "Codex AI Daily Briefing" | Select-Object LastRunTime,LastTaskResult,NextRunTime
```

See:

- [codex_scheduler/README.md](./codex_scheduler/README.md)
- [codex_scheduler/README.zh-CN.md](./codex_scheduler/README.zh-CN.md)

## Notes

- Feishu delivery requires either local `lark-cli` or Feishu API credentials.
- The Codex scheduler is intended for a trusted personal machine.
- The skill documentation also explains how to fork this AI-focused workflow into other domains such as business, finance, or policy.

For repository maintenance and publishing notes, see:

- [GITHUB_PUBLISHING.md](./GITHUB_PUBLISHING.md)
- [GITHUB_PUBLISHING.zh-CN.md](./GITHUB_PUBLISHING.zh-CN.md)
