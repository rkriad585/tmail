# Feature Addition Plan

## Overview
Add 6 features to tmail: view full message body, download attachments,
delete email from history, copy to clipboard, configurable poll interval,
and unread count badge.

## New dependency
- `pyperclip` — cross-platform clipboard access

## Files to modify

| File | Changes |
|------|---------|
| `pyproject.toml` | Add `pyperclip` to dependencies |
| `src/tmail/api.py` | Add `download_attachment()` |
| `src/tmail/storage.py` | Add config persistence, `delete_email()`, unread tracking |
| `src/tmail/ui.py` | Add full message view, email action submenu, settings UI, expanded email table with unread badge |
| `src/tmail/cli.py` | Add email action submenu, wire all new features, integrate unread badge |

## Implementation order

### 1. pyproject.toml
Add `pyperclip` to dependencies list.

### 2. api.py
- `download_attachment(att_id, save_path)` — stream attachment to file

### 3. storage.py
- `CONFIG_FILE` path, `load_config()`, `save_config()` — poll interval setting
- `delete_email(email)` — remove from old_mails.json
- `UNREAD_FILE` path, `save_unread_count(email, count)`, `get_unread_counts()` — per-email unread tracking
- `clear_unread_count(email)` — reset after viewing
- `remove_unread_entry(email)` — clean up when deleting email
- Move `DATA_DIR.mkdir` into helpers so individual functions are self-contained

### 4. ui.py
- `show_full_message(msg)` — Panel with From/To/Subject/body/attachments
- `get_email_actions_panel(email)` — submenu panel for email actions
- `show_messages_selection(messages)` — indexed table of messages for selection
- `get_settings_panel(poll_interval)` — settings display
- `show_emails_with_unread(emails, unread_counts)` — table with unread column

### 5. cli.py
- `email_actions_menu(email)` — submenu: view inbox, view message, download att, copy, delete, back
- `view_full_message(email)` — list messages, pick one, show full body
- `download_attachments(email)` — list messages with attachments, pick one, download
- `copy_to_clipboard(text)` — wrap pyperclip.copy with error handling
- `delete_email_saved()` — main menu: list saved emails, pick, confirm, delete
- `settings_menu()` — show current interval, option to change
- Update `main_menu()` — new options 4, 5, 6; pass poll_interval through
- Unread count displayed in menu listing and email table

## New menu layout

```
1. Generate Random Mail
2. See Mails You Created          (shows unread counts)
3. Log In To Old Mails
4. Delete Email From History
5. Remove All Old Mail's Data
6. Settings
7. Exit
```

After email inbox (options 1 or 3):

```
Email: <address>
1. View Inbox (live)
2. View Full Message
3. Download Attachments
4. Copy Email Address
5. Delete This Email
6. Back to Main Menu
```

## Data files
- `.temp_mail_data/config.json` — `{"poll_interval": 5}`
- `.temp_mail_data/unread.json` — `{"email@example.com": 3}`
- `.temp_mail_data/attachments/<email>/` — downloaded attachment files
