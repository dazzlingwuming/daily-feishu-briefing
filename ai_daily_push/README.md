[中文](./README.zh-CN.md) | English

# ai_daily_push

Standalone Python workflow for:

- fetching AI paper and AI news candidates
- deduplicating and ranking them
- rendering a Chinese daily briefing
- sending the final result to Feishu private chat

## Project Structure

- `app/sources/`
  Source adapters for arXiv and official blogs
- `app/pipeline/`
  normalization, scoring, dedup, selection, summarization
- `app/push/`
  rendering and Feishu senders
- `app/storage/`
  SQLite persistence and push history
- `scripts/`
  entrypoints and Windows task helpers
- `tests/`
  basic regression tests

## Quick Start

1. Copy `.env.example` to `.env`
2. Fill at least:
   - `FEISHU_SEND_MODE=cli`
   - `FEISHU_RECEIVER_OPEN_ID=your_open_id`
3. Initialize the local database:

```powershell
python scripts\init_db.py
```

4. Send a smoke test:

```powershell
python scripts\send_test_message.py --message "smoke test"
```

5. Run one daily pass:

```powershell
python scripts\run_once.py
```

6. If you want to ignore push history during manual verification:

```powershell
python scripts\run_once.py --ignore-history
```

## Useful Helper Scripts

- `scripts/export_candidates.py`
  Export normalized candidate items as JSON lines for manual inspection
- `scripts/send_test_message.py --file <path>`
  Send a UTF-8 text file directly through the configured Feishu sender

## Windows Scheduling

This project also includes a pure project-based scheduler:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_windows_task.ps1 -Time "09:00"
```

Remove it later with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_windows_task.ps1
```

## Delivery Modes

- `FEISHU_SEND_MODE=cli`
  Uses local `lark-cli`
- `FEISHU_SEND_MODE=api`
  Uses Feishu Open Platform app credentials

## Notes

- If `OPENAI_API_KEY` is empty, summarization falls back to local heuristic summaries.
- Generated briefings, local databases, and logs should not be committed.
