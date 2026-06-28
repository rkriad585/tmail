# tmail — Agent Guide

## One-liner

CLI TUI that creates temp emails via `api.internal.temp-mail.io` and live-polls the inbox.

## Setup & run

```bash
pip install uv
uv sync
tmail
```

Dependencies: `requests`, `rich`, `pyfiglet`, `pyperclip`.

## Entrypoint

`tmail.cli:main` (`pyproject.toml` → `[project.scripts]`). Also supports `python -m tmail` via `src/tmail/__main__.py`.

## Package structure

```
src/tmail/
├── __init__.py
├── __main__.py       # python -m tmail support
├── api.py            # HTTP client for temp-mail.io endpoints
├── cli.py            # CLI entry point, menu loop, inbox polling
├── storage.py        # JSON file persistence
└── ui.py             # Rich TUI components
tests/
└── __init__.py
```

## Data

`.temp_mail_data/` — created at runtime; stores `old_mails.json` (email history), `seen_mails.json` (fetched mail IDs), `config.json` (poll interval), and `unread.json` (per-email unread counts). Files read/written directly — no DB.

## Notable

- Rich `Live` with `auto_refresh=False` + manual `live.update(..., refresh=True)` on new mail only.
- pyfiglet `font="slant"` for banner.
- `remove_all_data` calls `Path.rmdir()` — only removes empty dirs; fails silently if dir has extra files.
- `pyperclip` used for clipboard copy; failure handled gracefully (no crash).
- Poll interval stored in `.temp_mail_data/config.json`; default 5s.
- Unread counts tracked per-email in `.temp_mail_data/unread.json`.
- After exiting inbox (Ctrl+C), an email action submenu opens: view full message, download attachments, copy address, delete email.

## API endpoints (internal, no auth)

- `POST https://api.internal.temp-mail.io/api/v3/email/new` — generate address
- `GET https://api.internal.temp-mail.io/api/v3/email/{email}/messages` — fetch inbox
- `GET https://api.internal.temp-mail.io/api/v3/attachment/{id}?download=1` — download link
