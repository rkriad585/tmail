# tmail — Agent Guide

## One-liner

CLI TUI that creates temp emails via `api.internal.temp-mail.io` and live-polls the inbox.

## Setup & run

```bash
pip install uv
uv sync
tmail
```

Dependencies: `requests`, `rich`, `pyfiglet`.

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

`.temp_mail_data/` — created at runtime; stores `old_mails.json` (email history) and `seen_mails.json` (fetched mail IDs). Files read/written directly — no DB.

## Testing

No tests written yet. Test runner not configured.

## API endpoints (internal, no auth)

- `POST https://api.internal.temp-mail.io/api/v3/email/new` — generate address
- `GET https://api.internal.temp-mail.io/api/v3/email/{email}/messages` — fetch inbox
- `GET https://api.internal.temp-mail.io/api/v3/attachment/{id}?download=1` — download link

## Notable

- Rich `Live` with `auto_refresh=False` + manual `live.update(..., refresh=True)` on new mail only.
- pyfiglet `font="slant"` for banner.
- `remove_all_data` calls `Path.rmdir()` — only removes empty dirs; fails silently if dir has extra files.
