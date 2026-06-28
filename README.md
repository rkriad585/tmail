<p align="center">
  <img src="https://img.shields.io/badge/tmail-v0.1.0-blue" alt="version">
  <img src="https://img.shields.io/badge/python-%3E%3D3.10-green" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="license">
</p>

<h1 align="center">📧 tmail</h1>
<p align="center"><em>Disposable email addresses, right from your terminal.</em></p>

---

## Overview

**tmail** is a lightweight CLI tool that generates temporary email addresses and
live-polls their inbox. Built with Python and the [Rich](https://github.com/Textualize/rich)
library, it gives you a disposable inbox without leaving your terminal.

## Installation

```bash
pip install uv
uv tool install tmail
```

Or install from source:

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

Select **1** to generate a new random email, then watch incoming mail arrive
in real time. Press **Ctrl+C** to return to the menu at any point.

## Command-line tool usage

```
tmail
```

Opens the interactive TUI menu:

1. **Generate Random Mail** — creates a new disposable address and opens its inbox
2. **See Mails You Created** — lists every address you have generated
3. **Log In To Old Mails** — re-opens the inbox of a previously created address
4. **Remove All Old Mail's Data** — deletes all stored email history
5. **Exit**

## How it works

tmail uses the internal [Temp Mail API](https://temp-mail.io/) (no authentication
required) to create addresses and fetch messages. Data is persisted locally in
`.temp_mail_data/` as JSON files.

## License

MIT
