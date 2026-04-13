[中文](./README.zh-CN.md) | English

# AI Daily Feishu Briefing

This repository contains two related workflows for delivering a daily AI papers and AI news briefing to Feishu private chat.

## What Is Included

- `skills/ai-daily-feishu-briefing/`
  The repository copy of the Codex skill source, including `SKILL.md`, references, helper scripts, and usage docs.
- `ai_daily_push/`
  A standalone Python project that fetches candidate items, ranks them, renders a Chinese briefing, and can send it through Feishu.
- `codex_scheduler/`
  A Codex-driven scheduler that uses the local `ai-daily-feishu-briefing` skill plus `codex exec` to generate the daily briefing into a UTF-8 file, then sends that file through the project sender.
- `项目.md`
  Earlier design notes in Chinese.

## Skill vs Project

This repo has both a skill-driven path and a normal project path.

### 1. Skill-driven path

Use this when you want Codex to do the final selection and writing.

Flow:

1. Windows Task Scheduler or manual PowerShell run
2. `codex_scheduler/run_codex_briefing.ps1`
3. `codex exec`
4. local skill: `ai-daily-feishu-briefing`
5. generate `ai_daily_push/briefing_feishu_today.txt`
6. send the file through the stable Feishu sender

This path is best when you want Codex to decide the final content.

### 2. Standalone project path

Use this when you want a direct Python workflow without depending on Codex at runtime.

Flow:

1. `ai_daily_push/scripts/run_once.py`
2. fetch candidates
3. deduplicate and rank
4. render briefing
5. send to Feishu

This path is best when you want a normal project that is easy to adapt.

## How To Use The Skill

The repository now includes the skill source here:

- `skills/ai-daily-feishu-briefing/`

To actually use it in Codex, install it into your local Codex skills directory so Codex can discover it. The scheduler assumes that the following skill is already available locally:

- `ai-daily-feishu-briefing`

Manual install example:

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<YourUser>\.codex\skills\ai-daily-feishu-briefing
```

Then start a new Codex session and trigger it with a prompt such as:

```text
Use $ai-daily-feishu-briefing to gather today's most important AI papers and AI news, write a Chinese briefing, and send it to my Feishu private chat.
```

See the skill usage guide:

- [skills/ai-daily-feishu-briefing/README.md](./skills/ai-daily-feishu-briefing/README.md)
- [skills/ai-daily-feishu-briefing/README.zh-CN.md](./skills/ai-daily-feishu-briefing/README.zh-CN.md)

That skill guide also explains how to fork this AI-focused skill into other themes such as business, finance, or policy briefings.

Typical manual run:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

Typical scheduled run:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "08:30"
```

Stop the scheduled task later:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

## How To Use The Project

See:

- [ai_daily_push/README.md](./ai_daily_push/README.md)
- [ai_daily_push/README.zh-CN.md](./ai_daily_push/README.zh-CN.md)

Quick example:

```powershell
cd ai_daily_push
python scripts\init_db.py
python scripts\send_test_message.py --message "smoke test"
python scripts\run_once.py --ignore-history
```

## Recommended Public Upload Scope

Safe and useful to upload:

- `skills/ai-daily-feishu-briefing/`
- `ai_daily_push/`
- `codex_scheduler/`
- `README.md`
- `README.zh-CN.md`
- `GITHUB_PUBLISHING.md`
- `GITHUB_PUBLISHING.zh-CN.md`
- `项目.md` if you want to keep the original design document

Do not upload:

- any real `.env`
- any real Feishu credential or receiver ID
- generated `*.db`
- generated briefing text files
- scheduler logs
- IDE folders and Python cache files

The included `.gitignore` already excludes the local and generated artifacts above.

## Before Publishing

1. Confirm `.env` is not committed.
2. Confirm no real `open_id`, app secret, or access token appears in docs or examples.
3. Confirm `codex_scheduler/logs/` is excluded.
4. Confirm generated files like `briefing_feishu_today.txt` are excluded.
5. Optionally replace machine-specific paths in docs if you want the repo to look cleaner for others.
