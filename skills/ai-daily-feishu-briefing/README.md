[中文](./README.zh-CN.md) | English

# ai-daily-feishu-briefing Skill

This folder contains the repository copy of the Codex skill source.

## What It Does

Use this skill when Codex should:

- gather today's AI papers and AI news
- choose the highest-signal items
- write a concise Chinese briefing
- send the result to Feishu private chat

It can also help build or modify the supporting Python project and scheduler, but its primary purpose is direct briefing delivery.

## Repository Copy vs Installed Skill

This folder is the source copy stored in Git.

Codex does not automatically load skills from this repository path. To use it in Codex, install or copy this folder into your local Codex skills directory.

Typical local install path:

```text
C:\Users\<YourUser>\.codex\skills\ai-daily-feishu-briefing
```

## Installation

From the repository root:

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<YourUser>\.codex\skills\ai-daily-feishu-briefing
```

Then start a new Codex session so the skill can be discovered.

## How To Trigger It

Example prompt:

```text
Use $ai-daily-feishu-briefing to gather today's most important AI papers and AI news, summarize them in Chinese, and send the final briefing to my Feishu private chat.
```

Focused example:

```text
Use $ai-daily-feishu-briefing to select the top 3 AI papers and top 3 AI news items today, keep the summaries concise, and send the result to Feishu.
```

## How It Fits Into This Repository

- `skills/ai-daily-feishu-briefing/`
  Skill source and documentation
- `ai_daily_push/`
  Standalone Python workflow and stable Feishu sender
- `codex_scheduler/`
  Codex wrapper and Windows task integration

The recommended path in this repository is:

1. Codex uses this skill to select and write the briefing
2. the wrapper writes the result to `ai_daily_push/briefing_feishu_today.txt`
3. the project sender sends that UTF-8 file to Feishu

## Adapting It To Other Topics

If you want to reuse this pattern for business, finance, policy, or other domains, the cleanest approach is to duplicate this skill into a new folder and adjust the topic-specific files.

Change these first:

- `SKILL.md`
  Skill name, scope, sources, and default goal
- `references/codex-workflow.md`
  Selection logic and what counts as a high-signal item
- `references/prompting.md`
  Summary framing and `why_it_matters`
- `agents/openai.yaml`
  Display name and default prompt

Keep the shared delivery infrastructure unless the new domain truly needs something different.

## Included Files

- `SKILL.md`
  Skill body used by Codex
- `agents/openai.yaml`
  Local display metadata
- `references/`
  Architecture, workflow, Feishu, and prompting notes
- `scripts/doctor.py`
  Local prerequisite check
- `scripts/send_test_message.py`
  Feishu smoke-test helper
