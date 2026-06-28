<p align="center">
  <img src="https://img.shields.io/badge/tmail-v0.2.0-blue" alt="version">
  <img src="https://img.shields.io/badge/python-%3E%3D3.10-green" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="license">
</p>

<h1 align="center">📧 tmail</h1>
<p align="center"><em>Disposable email addresses, right from your terminal.</em></p>

---

tmail is a lightweight CLI tool that generates temporary email addresses
and live-polls their inbox. Built with Python and [Rich](https://github.com/Textualize/rich).

## Quick start

```bash
pip install tmail-cli
# or with uv:
pip install uv && uv tool install tmail-cli
tmail           # interactive TUI
```

## CLI flags

| Command | Description |
|---|---|
| `tmail` | Open the interactive TUI menu |
| `tmail -g` | Generate a new email, print it, copy to clipboard |
| `tmail -g -w` | Generate and immediately watch the new inbox |
| `tmail -g -i` | Generate and fetch inbox once (one-shot) |
| `tmail -l` | List saved emails with unread counts |
| `tmail -i <email>` | Fetch inbox once (plain text, good for scripts) |
| `tmail -w <email>` | Live-poll inbox (plain text, Ctrl+C to stop) |
| `tmail -d <email>` | Delete an email from history |
| `tmail -n <seconds>` | Set poll interval |
| `tmail -c` | Clear all stored data |
| `tmail -V` | Show version |
| `tmail -h` | Show help |

## Documentation

| Doc | What's inside |
|---|---|
| [User Guide](docs/guide.md) | Full feature walkthrough, menu reference, settings, clipboard, attachments |
| [Development Guide](docs/development.md) | Architecture, module breakdown, code examples, adding features |

## Data

All data is stored in `.tmail_data/` as JSON files — no database required.

## License

MIT
