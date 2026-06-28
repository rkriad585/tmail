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
        "[4] Remove All Old Mail's Data\n"
        "[5] Exit",
        title="[bold cyan]Choose Your Option[/bold cyan]",
        border_style="blue",
    )


def show_emails_table(emails):
    """Displays a list of emails in a table."""
    if not emails:
        console.print("[yellow]No old emails found.[/yellow]")
        return

    table = Table(title="[bold green]Your Created Emails[/bold green]")
    table.add_column("Index", style="cyan")
    table.add_column("Email Address", style="magenta")

    for i, email in enumerate(emails, 1):
        table.add_row(str(i), email)

    console.print(table)


def show_inbox_header(email):
    """Prints the inbox header for a given email."""
    console.print(Panel(f"Inbox for: [bold green]{email}[/bold green]", expand=False))
    console.print("[dim]Press Ctrl+C to go back to the main menu...[/dim]")


def build_inbox_table(messages, seen_ids, attachment_url_fn):
    """Builds a Rich table from fetched messages, filtering seen IDs."""
    table = Table(title="[bold blue]Inbox[/bold blue]")
    table.add_column("From", style="cyan")
    table.add_column("To", style="cyan")
    table.add_column("Subject", style="magenta")
    table.add_column("Body", style="white")
    table.add_column("Attachments", style="yellow")

    new_messages = False
    for msg in messages:
        msg_id = str(msg["id"])
        if msg_id in seen_ids:
            continue
        new_messages = True
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

    return table, new_messages


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
