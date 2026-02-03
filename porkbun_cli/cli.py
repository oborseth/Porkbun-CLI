"""Main CLI application for Porkbun."""

import typer
from rich.console import Console
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import (
    print_success,
    print_error,
    print_info,
    create_table,
    format_price,
    console
)
from porkbun_cli.commands import (
    config_cmd,
    domain_cmd,
    dns_cmd,
    ssl_cmd,
    forward_cmd,
    glue_cmd,
    dnssec_cmd
)

app = typer.Typer(
    name="porkbun",
    help="Porkbun CLI - Manage domains and DNS via the Porkbun API",
    add_completion=False,
)

# Add command groups
app.add_typer(config_cmd.app, name="config")
app.add_typer(domain_cmd.app, name="domain")
app.add_typer(dns_cmd.app, name="dns")
app.add_typer(ssl_cmd.app, name="ssl")
app.add_typer(forward_cmd.app, name="forward")
app.add_typer(glue_cmd.app, name="glue")
app.add_typer(dnssec_cmd.app, name="dnssec")


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from porkbun_cli import __version__
        console.print(f"Porkbun CLI v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """
    Porkbun CLI - A powerful command-line interface for managing domains and DNS.

    Get started by configuring your API credentials:

        porkbun config set

    Then list your domains:

        porkbun domain list

    For help with a specific command:

        porkbun [COMMAND] --help
    """
    pass


@app.command()
def ping():
    """Test API connectivity and show your IP address."""
    config_manager = ConfigManager()

    try:
        apikey, secret = config_manager.get_credentials()
        config = config_manager.load()
        client = PorkbunClient(apikey, secret, config.base_url)

        result = client.ping()

        if result.get("status") == "SUCCESS":
            print_success("API connection successful!")
            if "yourIp" in result:
                print_info(f"Your IP address: {result['yourIp']}")
        else:
            print_error("API connection failed")

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command()
def pricing(
    search: str = typer.Option(None, "--search", "-s", help="Filter by TLD"),
    limit: int = typer.Option(10000, "--limit", "-l", help="Maximum number of results to display")
):
    """Show pricing for all TLDs."""
    config_manager = ConfigManager()
    config = config_manager.load()
    client = PorkbunClient("", "", config.base_url)  # Pricing doesn't require auth

    try:
        result = client.get_pricing()
        pricing_data = result.get("pricing", {})

        if not pricing_data:
            print_info("No pricing data available")
            return

        # Filter if search term provided
        if search:
            pricing_data = {
                tld: prices
                for tld, prices in pricing_data.items()
                if search.lower() in tld.lower()
            }

        if not pricing_data:
            print_info(f"No TLDs found matching '{search}'")
            return

        # Sort by TLD and limit results
        sorted_tlds = sorted(pricing_data.items())[:limit]

        table = create_table(
            "Porkbun Pricing",
            ["TLD", "Registration", "Renewal", "Transfer"]
        )

        for tld, prices in sorted_tlds:
            # Pricing API returns dollar amounts as strings, not pennies
            reg = prices.get("registration", "0")
            ren = prices.get("renewal", "0")
            trans = prices.get("transfer", "0")

            table.add_row(
                f".{tld}",
                f"${reg}" if reg else "N/A",
                f"${ren}" if ren else "N/A",
                f"${trans}" if trans else "N/A"
            )

        console.print(table)

        if len(pricing_data) > limit:
            print_info(f"Showing {limit} of {len(pricing_data)} TLDs. Use --limit to see more.")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
