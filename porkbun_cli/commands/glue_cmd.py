"""Glue record commands."""

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
    console
)

app = typer.Typer(help="Manage glue records")


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
def list_glue(domain: str):
    """List all glue records for a domain."""
    client = get_client()

    try:
        result = client.list_glue_records(domain)
        glue_records = result.get("glue", [])

        if not glue_records:
            print_info(f"No glue records found for '{domain}'")
            return

        table = create_table(
            f"Glue Records for {domain}",
            ["Subdomain", "IP Addresses"]
        )

        for glue in glue_records:
            subdomain = glue.get("subdomain", "N/A")
            ips = ", ".join(glue.get("ips", []))
            table.add_row(subdomain, ips)

        console.print(table)
        print_success(f"Found {len(glue_records)} glue record(s)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("create")
def create_glue(
    domain: str,
    subdomain: str = typer.Argument(..., help="Subdomain for glue record"),
    ips: list[str] = typer.Option(None, "--ip", help="IP address (can be specified multiple times)")
):
    """Create a glue record."""
    client = get_client()

    # Prompt for IPs if none provided
    if not ips:
        print_info("Enter IP addresses (comma-separated)")
        ips_input = prompt_string("IP addresses")
        ips = [ip.strip() for ip in ips_input.split(",")]

    if not ips:
        print_error("At least one IP address is required")
        raise typer.Exit(1)

    try:
        result = client.create_glue_record(domain, subdomain, ips)
        print_success(f"Glue record created for '{subdomain}.{domain}'")
        print_info(f"IP addresses: {', '.join(ips)}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("update")
def update_glue(
    domain: str,
    subdomain: str = typer.Argument(..., help="Subdomain for glue record"),
    ips: list[str] = typer.Option(None, "--ip", help="IP address (can be specified multiple times)")
):
    """Update a glue record."""
    client = get_client()

    # Prompt for IPs if none provided
    if not ips:
        print_info("Enter IP addresses (comma-separated)")
        ips_input = prompt_string("IP addresses")
        ips = [ip.strip() for ip in ips_input.split(",")]

    if not ips:
        print_error("At least one IP address is required")
        raise typer.Exit(1)

    try:
        result = client.update_glue_record(domain, subdomain, ips)
        print_success(f"Glue record updated for '{subdomain}.{domain}'")
        print_info(f"New IP addresses: {', '.join(ips)}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("delete")
def delete_glue(
    domain: str,
    subdomain: str = typer.Argument(..., help="Subdomain for glue record"),
    yes: bool = typer.Option(True, "--yes/--no-yes", "-y", help="Skip confirmation (default: yes)")
):
    """Delete a glue record."""
    client = get_client()

    if not yes:
        if not confirm(f"Delete glue record for '{subdomain}.{domain}'?", default=False):
            print_info("Deletion cancelled")
            return

    try:
        result = client.delete_glue_record(domain, subdomain)
        print_success(f"Glue record deleted for '{subdomain}.{domain}'")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
