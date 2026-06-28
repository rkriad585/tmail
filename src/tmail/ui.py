from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import pyfiglet

console = Console()


def show_logo():
    """Displays the application logo and welcome panel."""
    console.clear()
    banner = pyfiglet.figlet_format("tMail", font="slant")
    console.print(f"[bold green]{banner}[/bold green]")
    logo = Panel(
        "[dim]Your disposable email solution[/dim]",
        title="[bold cyan]Welcome[/bold cyan]",
        border_style="green",
        expand=False,
    )
    console.print(logo)


def get_main_menu_panel():
    """Returns the main menu options panel."""
    return Panel(
        "[1] Generate Random Mail\n"
        "[2] See Mails You Created\n"
        "[3] Log In To Old Mails\n"
        "[4] Delete Email From History\n"
        "[5] Remove All Old Mail's Data\n"
        "[6] Settings\n"
        "[7] Exit",
        title="[bold cyan]Choose Your Option[/bold cyan]",
        border_style="blue",
    )


def get_email_actions_panel(email):
    """Returns the email action submenu panel."""
    return Panel(
        "[1] View Inbox (live)\n"
        "[2] View Full Message\n"
        "[3] Download Attachments\n"
        "[4] Copy Email Address\n"
        "[5] Delete This Email\n"
        "[6] Back to Main Menu",
        title=f"[bold cyan]Email: {email}[/bold cyan]",
        border_style="blue",
    )


def get_settings_panel(poll_interval):
    """Returns the settings menu panel."""
    return Panel(
        f"Poll interval: [bold]{poll_interval}s[/bold]\n\n"
        "[1] Change Poll Interval\n"
        "[2] Back to Main Menu",
        title="[bold cyan]Settings[/bold cyan]",
        border_style="blue",
    )


def show_emails_with_unread(emails, unread_counts):
    """Displays a list of emails with unread counts in a table."""
    if not emails:
        console.print("[yellow]No old emails found.[/yellow]")
        return

    table = Table(title="[bold green]Your Created Emails[/bold green]")
    table.add_column("Index", style="cyan")
    table.add_column("Email Address", style="magenta")
    table.add_column("Unread", style="yellow", justify="right")

    for i, email in enumerate(emails, 1):
        count = unread_counts.get(email, 0)
        badge = str(count) if count else ""
        table.add_row(str(i), email, badge)

    console.print(table)


def show_emails_table(emails):
    """Displays a simple list of emails without unread counts."""
    show_emails_with_unread(emails, {})


def show_inbox_header(email):
    """Prints the inbox header for a given email."""
    console.print(Panel(f"Inbox for: [bold green]{email}[/bold green]", expand=False))
    console.print("[dim]Press Ctrl+C to go back to the email menu...[/dim]")


def build_inbox_table(messages, seen_ids, attachment_url_fn):
    """Builds a Rich table from fetched messages, filtering seen IDs.

    Returns (table, has_new_messages, new_count).
    """
    table = Table(title="[bold blue]Inbox[/bold blue]")
    table.add_column("From", style="cyan")
    table.add_column("To", style="cyan")
    table.add_column("Subject", style="magenta")
    table.add_column("Body", style="white")
    table.add_column("Attachments", style="yellow")

    new_count = 0
    for msg in messages:
        msg_id = str(msg["id"])
        if msg_id in seen_ids:
            continue
        new_count += 1
        seen_ids.add(msg_id)

        attachments = []
        if msg.get("attachments"):
            for att in msg["attachments"]:
                download_url = attachment_url_fn(att["id"])
                attachments.append(f"[link={download_url}]{att['name']}[/link]")

        body = msg["body_text"]
        if len(body) > 100:
            body = body[:100] + "..."

        table.add_row(
            msg["from"],
            msg["to"],
            msg["subject"],
            body,
            "\n".join(attachments) if attachments else "None",
        )

    return table, new_count > 0, new_count


def show_full_message(msg):
    """Displays a single message with full body in a Panel."""
    header = (
        f"[bold]From:[/bold] {msg['from']}\n"
        f"[bold]To:[/bold] {msg['to']}\n"
        f"[bold]Subject:[/bold] {msg['subject']}\n"
    )
    body = msg["body_text"]
    content = f"{header}\n{body}"

    if msg.get("attachments"):
        att_names = ", ".join(a["name"] for a in msg["attachments"])
        content += f"\n\n[bold]Attachments:[/bold] {att_names}"

    console.print(Panel(content, title="[bold cyan]Message[/bold cyan]", border_style="cyan"))


def show_messages_selection(messages):
    """Displays an indexed table of messages for selection.

    Returns list of (index, message) tuples.
    """
    table = Table(title="[bold blue]Messages[/bold blue]")
    table.add_column("Idx", style="cyan")
    table.add_column("From", style="cyan")
    table.add_column("Subject", style="magenta")
    table.add_column("Attachments", style="yellow")

    for i, msg in enumerate(messages, 1):
        att_count = len(msg.get("attachments") or [])
        att_text = f"{att_count} file(s)" if att_count else "None"
        table.add_row(str(i), msg["from"], msg["subject"], att_text)

    console.print(table)


def ask_choice(prompt_text, choices, default="1", **kwargs):
    """Prompts the user to make a choice from a list."""
    return Prompt.ask(prompt_text, choices=choices, default=default, **kwargs)


def wait_for_enter():
    """Waits for the user to press Enter."""
    Prompt.ask("[bold]Press Enter to go back...[/bold]")


def show_error(message):
    """Prints an error message in red."""
    console.print(f"[bold red]{message}[/bold red]")


def show_success(message):
    """Prints a success message in green."""
    console.print(f"[bold green]{message}[/bold green]")


def show_info(message):
    """Prints an informational message in yellow."""
    console.print(f"[bold yellow]{message}[/bold yellow]")
