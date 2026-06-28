import sys
import time
import json

import requests
from rich.live import Live

from .api import get_random_email, fetch_messages, get_attachment_url
from .storage import (
    save_email,
    get_old_emails,
    load_seen_mail_ids,
    save_seen_mail_ids,
    remove_all_data,
)
from .ui import (
    show_logo,
    get_main_menu_panel,
    show_emails_table,
    show_inbox_header,
    build_inbox_table,
    ask_choice,
    wait_for_enter,
    show_error,
    show_success,
    show_info,
    console,
)


def display_inbox(email):
    """Displays the inbox for a given email address with live polling."""
    show_inbox_header(email)

    seen_mail_ids = load_seen_mail_ids()

    with Live(console=console, screen=False, auto_refresh=False) as live:
        while True:
            try:
                messages = fetch_messages(email)
                table, new_messages = build_inbox_table(
                    messages, seen_mail_ids, get_attachment_url
                )

                if new_messages:
                    live.update(table, refresh=True)
                    save_seen_mail_ids(seen_mail_ids)

                time.sleep(5)
            except requests.RequestException as e:
                show_error(f"Error fetching inbox: {e}")
                time.sleep(5)
            except KeyboardInterrupt:
                break
            except json.JSONDecodeError:
                time.sleep(5)


def login_to_old_email():
    """Allows the user to select an old email to log in to."""
    old_emails = get_old_emails()
    if not old_emails:
        show_info("No old emails to log in to.")
        return None

    show_emails_table(old_emails)
    choice = ask_choice(
        "[bold]Enter the index of the email to restore[/bold]",
        choices=[str(i) for i in range(1, len(old_emails) + 1)],
        show_choices=False,
    )
    return old_emails[int(choice) - 1]


def main_menu():
    """Displays the main menu and handles user choices."""
    while True:
        show_logo()
        console.print(get_main_menu_panel())

        choice = ask_choice(
            "[bold]Choose an option[/bold]",
            choices=["1", "2", "3", "4", "5"],
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
            display_inbox(email)
        elif choice == "2":
            emails = get_old_emails()
            show_emails_table(emails)
            wait_for_enter()
        elif choice == "3":
            email = login_to_old_email()
            if email:
                display_inbox(email)
        elif choice == "4":
            remove_all_data()
            wait_for_enter()
        elif choice == "5":
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
