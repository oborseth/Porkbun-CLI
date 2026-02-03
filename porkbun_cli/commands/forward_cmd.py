"""URL forwarding commands."""

from typing import Optional
import typer
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import (
    print_success,
    print_error,
    print_info,
    create_table,
    confirm,
    prompt_string,
    prompt_choice,
    console
)

app = typer.Typer(help="Manage URL forwarding")


def get_client() -> PorkbunClient:
    """Get configured API client."""
    config_manager = ConfigManager()
    try:
        apikey, secret = config_manager.get_credentials()
        config = config_manager.load()
        return PorkbunClient(apikey, secret, config.base_url)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("list")
def list_forwards(domain: str):
    """List all URL forwards for a domain."""
    client = get_client()

    try:
        result = client.list_url_forwards(domain)
        forwards = result.get("forwards", [])

        if not forwards:
            print_info(f"No URL forwards found for '{domain}'")
            return

        table = create_table(
            f"URL Forwards for {domain}",
            ["ID", "Subdomain", "Location", "Type", "Wildcard"]
        )

        for forward in forwards:
            table.add_row(
                forward.get("id", "N/A"),
                forward.get("subdomain", "") or "(root)",
                forward.get("location", "N/A")[:50],
                forward.get("type", "N/A"),
                "Yes" if forward.get("wildcard") == "yes" else "No"
            )

        console.print(table)
        print_success(f"Found {len(forwards)} forward(s)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("add")
def add_forward(
    domain: str,
    location: Optional[str] = typer.Option(None, "--location", "-l", help="Target URL"),
    subdomain: Optional[str] = typer.Option(None, "--subdomain", "-s", help="Subdomain (leave empty for root)"),
    forward_type: str = typer.Option("temporary", "--type", "-t", help="Forward type (temporary or permanent)"),
    include_path: bool = typer.Option(False, "--include-path", help="Include request path in forward"),
    wildcard: bool = typer.Option(False, "--wildcard", help="Enable wildcard forwarding")
):
    """Add a URL forward for a domain."""
    client = get_client()

    # Prompt for location if not provided
    if location is None:
        location = prompt_string("Target URL (e.g., https://example.com)")

    if forward_type not in ["temporary", "permanent"]:
        print_error("Forward type must be 'temporary' or 'permanent'")
        raise typer.Exit(1)

    try:
        result = client.add_url_forward(
            domain=domain,
            subdomain=subdomain,
            location=location,
            forward_type=forward_type,
            include_path=include_path,
            wildcard=wildcard
        )

        forward_id = result.get("id")
        print_success(f"URL forward created successfully!")
        if forward_id:
            print_info(f"Forward ID: {forward_id}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("delete")
def delete_forward(
    domain: str,
    record_id: str,
    yes: bool = typer.Option(True, "--yes/--no-yes", "-y", help="Skip confirmation (default: yes)")
):
    """Delete a URL forward."""
    client = get_client()

    if not yes:
        if not confirm(f"Delete URL forward '{record_id}' from '{domain}'?", default=False):
            print_info("Deletion cancelled")
            return

    try:
        result = client.delete_url_forward(domain, record_id)
        print_success(f"URL forward '{record_id}' deleted successfully!")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
