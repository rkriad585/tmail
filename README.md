<p align="center">
  <img src="https://img.shields.io/badge/tmail-v0.1.0-blue" alt="version">
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
pip install uv
uv tool install tmail
tmail
```

Select **1** to generate a new email and watch mail arrive in real time.
Press **Ctrl+C** to open the email action menu.

## Documentation

| Doc | What's inside |
|---|---|
| [User Guide](docs/guide.md) | Full feature walkthrough, menu reference, settings, clipboard, attachments |
| [Development Guide](docs/development.md) | Architecture, module breakdown, code examples, adding features |

## Data

All data is stored in `.tmail_data/` as JSON files — no database required.

## License

MIT
