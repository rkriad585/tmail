# TempMail — Agent Guide

## One-liner

CLI TUI that creates temp emails via `api.internal.temp-mail.io` and live-polls the inbox.

## Setup & run

```bash
pip install uv
uv sync
tmail
```

Dependencies: `requests`, `rich`, `pyfiglet`.

## Project structure

- `mail.py` — single-file app: entrypoint, menu loop, API calls, TUI rendering, persistence.
- `.temp_mail_data/` — created at runtime; stores `old_mails.json` (history) and `seen_mails.json` (fetched mail IDs).

## Testing

No tests exist. No test runner configured.

## Key API endpoints (internal, no auth)

- `POST https://api.internal.temp-mail.io/api/v3/email/new` — generate address.
- `GET https://api.internal.temp-mail.io/api/v3/email/{email}/messages` — fetch inbox.
- `GET https://api.internal.temp-mail.io/api/v3/attachment/{id}?download=1` — download link.

## Notable

- Rich `Live` with `auto_refresh=False` + manual `live.update(..., refresh=True)` on new mail only.
- pyfiglet `font="slant"` for banner.
- JSON files are read/written directly (no DB).
- `remove_all_data` uses `Path.rmdir()` — will fail silently if dir has unexpected extra files.
