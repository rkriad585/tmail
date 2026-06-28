import json
from pathlib import Path

DATA_DIR = Path(".tmail_data")
OLD_MAILS_FILE = DATA_DIR / "old_mails.json"
SEEN_MAILS_FILE = DATA_DIR / "seen_mails.json"
CONFIG_FILE = DATA_DIR / "config.json"
UNREAD_FILE = DATA_DIR / "unread.json"
ATTACHMENTS_DIR = DATA_DIR / "attachments"


# --- Email history ---

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


def delete_email(email):
    """Removes a specific email from the history. Returns True if found."""
    emails = get_old_emails()
    if email not in emails:
        return False
    emails.remove(email)
    with open(OLD_MAILS_FILE, "w") as f:
        json.dump(emails, f, indent=4)
    return True


# --- Seen mail IDs ---

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


# --- Unread counts ---

def save_unread_count(email, count):
    """Saves the unread message count for an email address."""
    DATA_DIR.mkdir(exist_ok=True)
    data = {}
    if UNREAD_FILE.exists():
        with open(UNREAD_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    data[email] = count
    with open(UNREAD_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_unread_counts():
    """Returns the dict of email -> unread count."""
    if not UNREAD_FILE.exists():
        return {}
    with open(UNREAD_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def clear_unread_count(email):
    """Resets the unread count for an email to zero."""
    save_unread_count(email, 0)


def remove_unread_entry(email):
    """Removes the unread tracking entry for an email."""
    data = get_unread_counts()
    if email in data:
        del data[email]
        with open(UNREAD_FILE, "w") as f:
            json.dump(data, f, indent=4)


# --- Config ---

def load_config():
    """Loads user settings from config file."""
    if not CONFIG_FILE.exists():
        return {"poll_interval": 5}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"poll_interval": 5}


def save_config(config):
    """Saves user settings to config file."""
    DATA_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


# --- Cleanup ---

def remove_all_data():
    """Removes all stored data files and the data directory."""
    for p in [OLD_MAILS_FILE, SEEN_MAILS_FILE, CONFIG_FILE, UNREAD_FILE]:
        if p.exists():
            p.unlink()
    if ATTACHMENTS_DIR.exists():
        import shutil
        shutil.rmtree(ATTACHMENTS_DIR)
    if DATA_DIR.exists():
        try:
            DATA_DIR.rmdir()
        except OSError:
            pass
