# tmail Development Guide

## Project structure

```
src/tmail/
├── __init__.py       # Package marker (empty)
├── __main__.py       # python -m tmail support
├── api.py            # HTTP client for temp-mail.io
├── cli.py            # Entry point, menu loop, orchestration
├── storage.py        # JSON file persistence
└── ui.py             # Rich TUI components
tests/
└── __init__.py
```

## Module responsibilities

### api.py — HTTP client

Pure functions that call the temp-mail.io API. No UI, no state.

```python
from tmail.api import get_random_email, fetch_messages, download_attachment

email = get_random_email()
messages = fetch_messages(email)
download_attachment("att_id", Path("/tmp/file.pdf"))
```

Endpoints:

| Function | Method | Endpoint |
|---|---|---|
| `get_random_email()` | POST | `/api/v3/email/new` |
| `fetch_messages(email)` | GET | `/api/v3/email/{email}/messages` |
| `get_attachment_url(id)` | — | returns URL string |
| `download_attachment(id, path)` | GET (stream) | `/api/v3/attachment/{id}?download=1` |

### storage.py — persistence

Read/write JSON files in `.tmail_data/`. Every function is self-contained
(calls `DATA_DIR.mkdir` when needed).

```python
from tmail.storage import save_email, get_old_emails, delete_email

save_email("foo@example.com")
emails = get_old_emails()
deleted = delete_email("foo@example.com")
```

Config:

```python
from tmail.storage import load_config, save_config

cfg = load_config()           # {"poll_interval": 5}
save_config({"poll_interval": 3})
```

Unread tracking:

```python
from tmail.storage import save_unread_count, get_unread_counts, clear_unread_count

save_unread_count("foo@example.com", 3)
counts = get_unread_counts()          # {"foo@example.com": 3}
clear_unread_count("foo@example.com")
```

### ui.py — rendering

Thin wrappers around Rich that format output. No logic, no API calls.

```python
from tmail.ui import console, show_logo, show_success, show_error, build_inbox_table

show_logo()
show_success("Email created")
table, has_new, count = build_inbox_table(messages, seen_ids, get_attachment_url)
```

Key components:

- `show_logo()` — pyfiglet banner + welcome panel
- `build_inbox_table()` — returns `(Table, has_new, new_count)`
- `show_full_message(msg)` — Panel with full body text
- `show_messages_selection(messages)` — indexed table for picking a message
- `get_email_actions_panel(email)` — returns the action submenu Panel
- `get_main_menu_panel()` — returns the main menu Panel
- `get_settings_panel(interval)` — returns the settings Panel

### cli.py — orchestration

Wires api/storage/ui together. Contains the main loop, inbox poller, all
submenus, and CLI flag handling via `argparse`. This is the entry point
(`tmail.cli:main`).

```python
from tmail.cli import main

main()  # parses sys.argv, dispatches flags or starts TUI
```

Flow:

```
main() → argparse → --generate / --list / --inbox / --watch / ...
                 ↘ main_menu() → email actions → display_inbox()
                              ↘ settings_menu()
                              ↘ delete_email_saved()
```

CLI flags are defined in `main()` using `argparse.ArgumentParser`. Each
flag calls the same core functions from api/storage/ui but uses plain
`print()` instead of Rich widgets so output works in pipes and scripts.

Non-interactive helpers:

| Function | Used by |
|---|---|
| `_print_messages_plain(messages)` | `--inbox`, `--watch` |
| `_copy_silent(text)` | `--generate` |
| (inline handlers) | `--list`, `--delete`, `--interval`, `--clear`, `--version` |

## Adding a new menu option

1. Add the label to `get_main_menu_panel()` in `ui.py`
2. Add a handler function in `cli.py`
3. Wire the choice in `main_menu()` switch

Example — adding a "Show Version" option:

```python
# ui.py — add to panel
"[5] Show Version\n"
"[6] Remove All Old Mail's Data\n"
"[7] Settings\n"
"[8] Exit",

# cli.py — add handler
def show_version():
    console.print("[bold]tmail v0.1.0[/bold]")
    wait_for_enter()

# cli.py — wire in main_menu
elif choice == "5":
    show_version()
```

## Adding a new email action

1. Add the label to `get_email_actions_panel()` in `ui.py`
2. Add a handler in `cli.py`
3. Wire the choice in `email_actions_menu()`

## Testing

No test framework is configured. To test manually:

```bash
uv run tmail
```

Or import and call individual modules:

```bash
uv run python -c "
from tmail.api import get_random_email
print(get_random_email())
"
```

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP client for temp-mail.io API |
| `rich` | Terminal UI (tables, panels, live view, prompts) |
| `pyfiglet` | ASCII art banner |
| `pyperclip` | Clipboard copy (cross-platform) |

## Data format reference

### old_mails.json

```json
["abc@tempmail.com", "def@tempmail.com"]
```

### seen_mails.json

```json
["msg-uuid-1", "msg-uuid-2"]
```

### config.json

```json
{"poll_interval": 5}
```

### unread.json

```json
{"abc@tempmail.com": 3}
```
