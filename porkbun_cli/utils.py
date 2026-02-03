"""Utility functions for Porkbun CLI."""

from typing import Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red]✗[/red] {message}", style="red")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]⚠[/yellow] {message}", style="yellow")


def print_json(data: dict[str, Any]) -> None:
    """Print JSON data in a formatted way."""
    console.print_json(data=data)


def create_table(title: str, columns: list[str]) -> Table:
    """Create a rich table with consistent styling.

    Args:
        title: Table title
        columns: List of column names

    Returns:
        Configured Table object
    """
    table = Table(
        title=title,
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="blue"
    )

    for column in columns:
        table.add_column(column)

    return table


def print_panel(content: str, title: str, style: str = "blue") -> None:
    """Print content in a panel.

    Args:
        content: Panel content
        title: Panel title
        style: Panel border style
    """
    panel = Panel(content, title=title, border_style=style, box=box.ROUNDED)
    console.print(panel)


def confirm(message: str, default: bool = False) -> bool:
    """Ask for user confirmation.

    Args:
        message: Confirmation message
        default: Default response

    Returns:
        True if confirmed, False otherwise
    """
    from rich.prompt import Confirm
    return Confirm.ask(message, default=default)


def prompt_string(message: str, default: str = None, password: bool = False) -> str:
    """Prompt for a string value.

    Args:
        message: Prompt message
        default: Default value
        password: Whether to hide input (for passwords)

    Returns:
        User input string
    """
    from rich.prompt import Prompt
    return Prompt.ask(message, default=default, password=password)


def prompt_int(message: str, default: int = None) -> int:
    """Prompt for an integer value.

    Args:
        message: Prompt message
        default: Default value

    Returns:
        User input integer
    """
    from rich.prompt import IntPrompt
    return IntPrompt.ask(message, default=default)


def prompt_choice(message: str, choices: list[str], default: str = None) -> str:
    """Prompt for a choice from a list.

    Args:
        message: Prompt message
        choices: List of valid choices
        default: Default choice

    Returns:
        Selected choice
    """
    from rich.prompt import Prompt
    return Prompt.ask(message, choices=choices, default=default)


def format_price(pennies: int) -> str:
    """Format price from pennies to dollars.

    Args:
        pennies: Price in pennies

    Returns:
        Formatted price string
    """
    dollars = pennies / 100
    return f"${dollars:.2f}"


def format_ttl(seconds: int) -> str:
    """Format TTL from seconds to human-readable format.

    Args:
        seconds: TTL in seconds

    Returns:
        Formatted TTL string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        return f"{seconds // 3600}h"
    else:
        return f"{seconds // 86400}d"
