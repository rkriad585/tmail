# tmail User Guide

## Installation

```bash
pip install uv
uv tool install tmail
```

Or from source:

```bash
git clone https://github.com/rkriad585/tmail.git
cd tmail
pip install uv
uv sync
```

## Quick start

```bash
tmail
```

Press **1** to generate a new random email, then watch incoming mail arrive
in real time. Press **Ctrl+C** to return to the email action menu.

## Main menu

```
╭───────────────────────────── Choose Your Option ─────────────────────────────╮
│ [1] Generate Random Mail                                                     │
│ [2] See Mails You Created                                                    │
│ [3] Log In To Old Mails                                                      │
│ [4] Delete Email From History                                                │
│ [5] Remove All Old Mail's Data                                               │
│ [6] Settings                                                                 │
│ [7] Exit                                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

| Option | Description |
|---|---|
| **1** | Generate a new disposable email address and open its inbox |
| **2** | List every address you have generated (shows unread counts) |
| **3** | Re-open the inbox of a previously created address |
| **4** | Select and delete a specific email from history |
| **5** | Wipe all stored data (history, seen IDs, config, unread counts) |
| **6** | Change the inbox polling interval |
| **7** | Exit |

## Email action submenu

After exiting an inbox (Ctrl+C), you return to this submenu:

```
╭───────────────────────────── Email: xxxxx@xxxxx.xx ──────────────────────────╮
│ [1] View Inbox (live)                                                        │
│ [2] View Full Message                                                        │
│ [3] Download Attachments                                                     │
│ [4] Copy Email Address                                                       │
│ [5] Delete This Email                                                        │
│ [6] Back to Main Menu                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

| Option | Description |
|---|---|
| **1** | Re-enter the live inbox poller |
| **2** | List messages by index, pick one to read the full body |
| **3** | List messages with attachments, pick one to download all files |
| **4** | Copy the email address to your clipboard |
| **5** | Remove this email from history |
| **6** | Return to the main menu |

## Inbox polling

The inbox refreshes every N seconds (default 5). Only new messages trigger a
screen update — the terminal stays quiet between polls. Configure the interval
in **Settings** (option 6).

## Settings

```
╭────────────────────────────────── Settings ──────────────────────────────────╮
│ Poll interval: 5s                                                            │
│                                                                              │
│ [1] Change Poll Interval                                                     │
│ [2] Back to Main Menu                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Choose **1** to enter a new interval in seconds (minimum 1).

## Clipboard

Option **4** in the email action submenu copies the email address to your
clipboard. On Linux, one of these must be installed:

- **X11:** `sudo apt install xclip` or `xsel`
- **Wayland:** `sudo apt install wl-clipboard`

Windows and macOS work out of the box.

## Attachments

Option **3** in the email action submenu lists messages that have attachments.
Pick one and all its files are downloaded to `.tmail_data/attachments/<email>/`.

## Data files

All data is stored in `.tmail_data/`:

| File | Purpose |
|---|---|
| `old_mails.json` | List of generated email addresses |
| `seen_mails.json` | IDs of messages already displayed |
| `config.json` | User settings (poll interval) |
| `unread.json` | Per-email unread message counts |
| `attachments/` | Downloaded attachment files |
