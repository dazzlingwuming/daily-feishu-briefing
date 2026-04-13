[中文](./README.zh-CN.md) | English

# ai-daily-feishu-briefing Skill

This folder contains the repository copy of the Codex skill source.

## What This Skill Is For

Use this skill when Codex should:

- gather today's AI papers and AI news
- select the highest-signal items
- write a concise Chinese briefing
- send the result to Feishu private chat

It can also help build or modify the underlying Python project and scheduler, but the primary mode is direct briefing delivery.

## Repository Source vs Installed Skill

This folder is the source copy stored in Git.

Codex does not load skills directly from this repository path by default. To use it in Codex, install or copy this folder into your local Codex skills directory.

Typical local install path:

```text
C:\Users\<YourUser>\.codex\skills\ai-daily-feishu-briefing
```

## How To Install

From the repository root:

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<YourUser>\.codex\skills\ai-daily-feishu-briefing
```

Then start a new Codex session so the skill can be discovered.

## How To Trigger It In Codex

Example prompt:

```text
Use $ai-daily-feishu-briefing to gather today's most important AI papers and AI news, summarize them in Chinese, and send the final briefing to my Feishu private chat.
```

More focused example:

```text
Use $ai-daily-feishu-briefing to select the top 3 AI papers and top 3 AI news items today, keep the summaries concise, and send the result to Feishu.
```

## How It Relates To This Repository

- `skills/ai-daily-feishu-briefing/`
  Skill source and documentation
- `ai_daily_push/`
  Standalone Python workflow and stable Feishu sender
- `codex_scheduler/`
  Codex wrapper and Windows task integration

The current recommended production-like path in this repo is:

1. Codex uses this skill to select and write the briefing
2. the wrapper writes the result to `ai_daily_push/briefing_feishu_today.txt`
3. the project sender sends that UTF-8 file to Feishu

## How To Adapt This Skill To Other Topics

You do not need to change the runtime architecture if you want to reuse this pattern for other domains such as business, finance, policy, or general industry news.

The cleanest approach is to duplicate this skill into a new folder and then adjust the topic-specific files.

Recommended approach:

1. Copy `skills/ai-daily-feishu-briefing/` to a new skill folder, for example:
   - `skills/business-daily-feishu-briefing/`
   - `skills/finance-daily-feishu-briefing/`
2. Rename the skill inside `SKILL.md`
3. Update the metadata in `agents/openai.yaml`
4. Replace the default sources, ranking rules, and summary framing in the reference files

Files you should change first:

- `SKILL.md`
  Change the skill name, scope, default sources, and default briefing goal
- `references/codex-workflow.md`
  Change how items are selected and what counts as a strong item in that domain
- `references/prompting.md`
  Change the summary style and the `why_it_matters` framing
- `agents/openai.yaml`
  Change the display name and default prompt

Typical examples:

- Business briefing:
  Focus on company strategy, product launches, partnerships, pricing, hiring, and market moves
- Finance briefing:
  Focus on earnings, capital markets, regulation, liquidity, valuation impact, and investor relevance
- Policy briefing:
  Focus on regulators, government announcements, enforcement, compliance, and downstream business impact

Keep these shared layers unless the new domain truly needs different code:

- `scripts/doctor.py`
- `scripts/send_test_message.py`
- the Feishu sending path
- the scheduler pattern in `codex_scheduler/`

In other words, most topic changes belong in the skill instructions and source-selection rules, not in the delivery infrastructure.

## Included Files

- `SKILL.md`
  Skill body used by Codex
- `agents/openai.yaml`
  Display metadata for the local skill
- `references/`
  Architecture, workflow, Feishu, and prompting notes
- `scripts/doctor.py`
  Check local prerequisites
- `scripts/send_test_message.py`
  Send a smoke-test message through Feishu

## Recommended Validation

```powershell
python .\skills\ai-daily-feishu-briefing\scripts\doctor.py --env-file .\ai_daily_push\.env
python .\skills\ai-daily-feishu-briefing\scripts\send_test_message.py --env-file .\ai_daily_push\.env --mode cli --message "skill smoke test"
```
