[中文](./README.zh-CN.md) | English

# ai_daily_push

`ai_daily_push` is the standalone Python implementation of the daily briefing workflow.

It is responsible for:

- fetching AI paper and AI news candidates
- deduplicating and ranking items
- rendering a Chinese briefing
- sending the result to Feishu private chat

## Directory Layout

- `app/sources/`
  Source adapters such as arXiv and official blog feeds
- `app/pipeline/`
  Normalize, deduplicate, score, select, and summarize
- `app/push/`
  Render the report and deliver it through Feishu
- `app/storage/`
  SQLite cache and push history
- `scripts/`
  Operational entrypoints and Windows task helpers
- `tests/`
  Basic regression tests

## Quick Start

1. Copy `.env.example` to `.env`
2. Set at least:
   - `FEISHU_SEND_MODE=cli`
   - `FEISHU_RECEIVER_OPEN_ID=your_open_id`
3. Initialize the database:

```powershell
python scripts\init_db.py
```

4. Send a smoke test:

```powershell
python scripts\send_test_message.py --message "smoke test"
```

5. Run one pass:

```powershell
python scripts\run_once.py
```

6. If you want to ignore push history during manual verification:

```powershell
python scripts\run_once.py --ignore-history
```

## Useful Scripts

- `scripts/export_candidates.py`
  Export normalized candidates as JSON lines for inspection
- `scripts/send_test_message.py --file <path>`
  Send a UTF-8 text file through the configured Feishu sender

## Scheduling

This project also includes a pure project-based Windows scheduled task flow:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_windows_task.ps1 -Time "09:00"
```

Remove it later:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_windows_task.ps1
```

## Delivery Modes

- `FEISHU_SEND_MODE=cli`
  Use local `lark-cli`
- `FEISHU_SEND_MODE=api`
  Use Feishu Open Platform app credentials

## Notes

- If `OPENAI_API_KEY` is empty, summarization falls back to local heuristic summaries.
- Generated briefings, databases, and runtime logs should stay out of version control.
