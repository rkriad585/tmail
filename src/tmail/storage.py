import json
from pathlib import Path

DATA_DIR = Path(".temp_mail_data")
OLD_MAILS_FILE = DATA_DIR / "old_mails.json"
SEEN_MAILS_FILE = DATA_DIR / "seen_mails.json"


def save_email(email):
    """Saves a generated email to the history."""
    DATA_DIR.mkdir(exist_ok=True)
    if not OLD_MAILS_FILE.exists():
        with open(OLD_MAILS_FILE, "w") as f:
            json.dump([], f)

    with open(OLD_MAILS_FILE, "r+") as f:
        try:
            emails = json.load(f)
        except json.JSONDecodeError:
            emails = []
        if email not in emails:
            emails.append(email)
            f.seek(0)
            json.dump(emails, f, indent=4)


def get_old_emails():
    """Retrieves the list of previously generated emails."""
    if not OLD_MAILS_FILE.exists():
        return []
    with open(OLD_MAILS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def load_seen_mail_ids():
    """Loads the set of seen mail IDs from disk."""
    if not SEEN_MAILS_FILE.exists():
        return set()
    with open(SEEN_MAILS_FILE, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()


def save_seen_mail_ids(ids):
    """Persists the set of seen mail IDs to disk."""
    with open(SEEN_MAILS_FILE, "w") as f:
        json.dump(list(ids), f)


def remove_all_data():
    """Removes all stored data files and the data directory."""
    if OLD_MAILS_FILE.exists():
        OLD_MAILS_FILE.unlink()
    if SEEN_MAILS_FILE.exists():
        SEEN_MAILS_FILE.unlink()
    if DATA_DIR.exists():
        try:
            DATA_DIR.rmdir()
        except OSError:
            pass
