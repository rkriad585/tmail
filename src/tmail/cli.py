import sys
import time
import json
from pathlib import Path

import requests
from rich.live import Live
from rich.prompt import Prompt

from .api import get_random_email, fetch_messages, get_attachment_url, download_attachment
from .storage import (
    save_email,
    get_old_emails,
    delete_email,
    load_seen_mail_ids,
    save_seen_mail_ids,
    save_unread_count,
    get_unread_counts,
    clear_unread_count,
    remove_unread_entry,
    load_config,
    save_config,
    remove_all_data,
    ATTACHMENTS_DIR,
)
from .ui import (
    show_logo,
    get_main_menu_panel,
    get_email_actions_panel,
    get_settings_panel,
    show_emails_with_unread,
    show_inbox_header,
    build_inbox_table,
    show_full_message,
    show_messages_selection,
    ask_choice,
    wait_for_enter,
    show_error,
    show_success,
    show_info,
    console,
)


def display_inbox(email, poll_interval):
    """Displays the inbox for a given email address with live polling.

    Returns the number of new messages received this session.
    """
    show_inbox_header(email)

    seen_mail_ids = load_seen_mail_ids()
    session_new_count = 0

    with Live(console=console, screen=False, auto_refresh=False) as live:
        while True:
            try:
                messages = fetch_messages(email)
                table, has_new, batch_count = build_inbox_table(
                    messages, seen_mail_ids, get_attachment_url
                )

                if has_new:
                    session_new_count += batch_count
                    live.update(table, refresh=True)
                    save_seen_mail_ids(seen_mail_ids)

                time.sleep(poll_interval)
            except requests.RequestException as e:
                show_error(f"Error fetching inbox: {e}")
                time.sleep(poll_interval)
            except KeyboardInterrupt:
                break
            except json.JSONDecodeError:
                time.sleep(poll_interval)

    return session_new_count


def view_full_message(email):
    """Fetch all messages and let the user pick one to read in full."""
    try:
        messages = fetch_messages(email)
    except requests.RequestException as e:
        show_error(f"Error fetching messages: {e}")
        return

    if not messages:
        show_info("No messages found.")
        return

    show_messages_selection(messages)
    choices = [str(i) for i in range(1, len(messages) + 1)]
    choice = ask_choice(
        "[bold]Enter message index to view[/bold]",
        choices=choices,
        show_choices=False,
    )
    msg = messages[int(choice) - 1]
    show_full_message(msg)
    wait_for_enter()


def download_attachments(email):
    """List messages with attachments and let the user download them."""
    try:
        messages = fetch_messages(email)
    except requests.RequestException as e:
        show_error(f"Error fetching messages: {e}")
        return

    with_attachments = [m for m in messages if m.get("attachments")]
    if not with_attachments:
        show_info("No messages with attachments found.")
        return

    show_messages_selection(with_attachments)
    choices = [str(i) for i in range(1, len(with_attachments) + 1)]
    choice = ask_choice(
        "[bold]Enter message index to download attachments[/bold]",
        choices=choices,
        show_choices=False,
    )
    msg = with_attachments[int(choice) - 1]
    atts = msg["attachments"]

    save_dir = ATTACHMENTS_DIR / email
    save_dir.mkdir(parents=True, exist_ok=True)

    for att in atts:
        dest = save_dir / att["name"]
        try:
            download_attachment(att["id"], dest)
            show_success(f"Downloaded: {att['name']}")
        except requests.RequestException as e:
            show_error(f"Failed to download {att['name']}: {e}")

    wait_for_enter()


def copy_to_clipboard(text):
    """Copy text to clipboard. Tries pyperclip first, then direct backends."""
    import subprocess
    import shutil

    try:
        import pyperclip
        pyperclip.copy(text)
        show_success(f"Copied to clipboard: {text}")
        wait_for_enter()
        return
    except Exception:
        pass

    backends = [
        ("xclip", ["xclip", "-selection", "clipboard"]),
        ("xsel", ["xsel", "--clipboard", "--input"]),
        ("wl-copy", ["wl-copy"]),
    ]

    for name, cmd in backends:
        if shutil.which(name):
            try:
                proc = subprocess.run(cmd, input=text, text=True, capture_output=True, timeout=5)
                if proc.returncode == 0:
                    show_success(f"Copied to clipboard: {text}")
                    wait_for_enter()
                    return
            except Exception:
                continue

    show_info(
        "Clipboard copy requires a clipboard tool.\n"
        "  X11: sudo apt install xclip   (or xsel)\n"
        "  Wayland: sudo apt install wl-clipboard"
    )
    wait_for_enter()


def email_actions_menu(email):
    """Submenu for actions on a specific email after exiting inbox."""
    config = load_config()
    poll_interval = config["poll_interval"]

    while True:
        show_logo()
        console.print(get_email_actions_panel(email))

        choice = ask_choice(
            "[bold]Choose an option[/bold]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="1",
        )

        if choice == "1":
            clear_unread_count(email)
            session_count = display_inbox(email, poll_interval)
            if session_count > 0:
                save_unread_count(email, session_count)
        elif choice == "2":
            view_full_message(email)
        elif choice == "3":
            download_attachments(email)
        elif choice == "4":
            copy_to_clipboard(email)
        elif choice == "5":
            if delete_email(email):
                remove_unread_entry(email)
                show_success(f"Deleted email: {email}")
                wait_for_enter()
                return
            show_error("Email not found in history.")
            wait_for_enter()
        elif choice == "6":
            return


def login_to_old_email():
    """Allows the user to select an old email to log in to."""
    old_emails = get_old_emails()
    if not old_emails:
        show_info("No old emails to log in to.")
        return None

    unread_counts = get_unread_counts()
    show_emails_with_unread(old_emails, unread_counts)
    choice = ask_choice(
        "[bold]Enter the index of the email to restore[/bold]",
        choices=[str(i) for i in range(1, len(old_emails) + 1)],
        show_choices=False,
    )
    return old_emails[int(choice) - 1]


def delete_email_saved():
    """Main menu: delete a specific email from history."""
    old_emails = get_old_emails()
    if not old_emails:
        show_info("No saved emails to delete.")
        wait_for_enter()
        return

    unread_counts = get_unread_counts()
    show_emails_with_unread(old_emails, unread_counts)
    choice = ask_choice(
        "[bold]Enter the index of the email to delete[/bold]",
        choices=[str(i) for i in range(1, len(old_emails) + 1)],
        show_choices=False,
    )
    email = old_emails[int(choice) - 1]

    confirm = Prompt.ask(
        f"Delete [bold]{email}[/bold]? (y/n)", choices=["y", "n"], default="n"
    )
    if confirm == "y":
        if delete_email(email):
            remove_unread_entry(email)
            show_success(f"Deleted email: {email}")
        else:
            show_error("Email not found in history.")
    wait_for_enter()


def settings_menu():
    """Settings menu for configuring poll interval."""
    config = load_config()

    while True:
        show_logo()
        console.print(get_settings_panel(config["poll_interval"]))

        choice = ask_choice(
            "[bold]Choose an option[/bold]",
            choices=["1", "2"],
            default="2",
        )

        if choice == "1":
            interval = Prompt.ask(
                "[bold]Poll interval in seconds[/bold]",
                default=str(config["poll_interval"]),
            )
            try:
                val = int(interval)
                if val < 1:
                    show_info("Minimum interval is 1 second.")
                    continue
                config["poll_interval"] = val
                save_config(config)
                show_success(f"Poll interval set to {val}s")
                wait_for_enter()
            except ValueError:
                show_error("Invalid number.")
                wait_for_enter()
        elif choice == "2":
            return


def main_menu():
    """Displays the main menu and handles user choices."""
    config = load_config()
    poll_interval = config["poll_interval"]

    while True:
        show_logo()
        console.print(get_main_menu_panel())

        choice = ask_choice(
            "[bold]Choose an option[/bold]",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            default="1",
        )

        if choice == "1":
            try:
                email = get_random_email()
            except requests.RequestException as e:
                show_error(f"Error generating email: {e}")
                continue
            save_email(email)
            show_success(f"Your new email is: {email}")
            session_count = display_inbox(email, poll_interval)
            if session_count > 0:
                save_unread_count(email, session_count)
            email_actions_menu(email)
        elif choice == "2":
            emails = get_old_emails()
            unread_counts = get_unread_counts()
            show_emails_with_unread(emails, unread_counts)
            wait_for_enter()
        elif choice == "3":
            email = login_to_old_email()
            if email:
                clear_unread_count(email)
                session_count = display_inbox(email, poll_interval)
                if session_count > 0:
                    save_unread_count(email, session_count)
                email_actions_menu(email)
        elif choice == "4":
            delete_email_saved()
        elif choice == "5":
            remove_all_data()
            show_success("Successfully removed all old mails data.")
            wait_for_enter()
        elif choice == "6":
            settings_menu()
            config = load_config()
            poll_interval = config["poll_interval"]
        elif choice == "7":
            console.print("[bold cyan]Thanks for using tmail! Goodbye![/bold cyan]")
            sys.exit()


def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold cyan]Goodbye![/bold cyan]")
        sys.exit(0)


if __name__ == "__main__":
    main()
