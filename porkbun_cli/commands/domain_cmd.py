"""Domain management commands."""

from typing import Optional
import typer
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import (
    print_success,
    print_error,
    print_info,
    print_warning,
    create_table,
    format_price,
    confirm,
    console
)

app = typer.Typer(help="Manage domains")


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
def list_domains(
    start: Optional[int] = typer.Option(None, help="Starting position for pagination"),
    include_labels: bool = typer.Option(False, "--include-labels", help="Include domain labels")
):
    """List all domains in your account."""
    client = get_client()

    try:
        result = client.list_domains(start=start, include_labels=include_labels)

        if "domains" not in result or not result["domains"]:
            print_info("No domains found in your account")
            return

        domains = result["domains"]
        table = create_table("Your Domains", ["Domain", "Status", "Auto-Renew", "Expires"])

        for domain in domains:
            table.add_row(
                domain.get("domain", "N/A"),
                domain.get("status", "N/A"),
                "Yes" if domain.get("autoRenew") == 1 else "No",
                domain.get("expireDate", "N/A")
            )

        console.print(table)
        print_success(f"Found {len(domains)} domain(s)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("check")
def check_domain(domain: str):
    """Check if a domain is available for registration."""
    client = get_client()

    try:
        result = client.check_domain(domain)

        available = result.get("availability") == "available"
        price_data = result.get("price", {})

        if available:
            registration = price_data.get("registration", 0)
            renewal = price_data.get("renewal", 0)

            print_success(f"Domain '{domain}' is available!")
            print_info(f"Registration: {format_price(registration)}")
            print_info(f"Renewal: {format_price(renewal)}")
        else:
            print_warning(f"Domain '{domain}' is not available")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("create")
def create_domain(
    domain: str,
    cost: int = typer.Option(..., help="Expected cost in pennies (for confirmation)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Register a new domain."""
    client = get_client()

    if not yes:
        if not confirm(
            f"Register domain '{domain}' for {format_price(cost)}?",
            default=False
        ):
            print_info("Registration cancelled")
            return

    try:
        result = client.create_domain(domain, cost)
        print_success(f"Domain '{domain}' registered successfully!")

        if "orderId" in result:
            print_info(f"Order ID: {result['orderId']}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("get-ns")
def get_nameservers(domain: str):
    """Get nameservers for a domain."""
    client = get_client()

    try:
        result = client.get_nameservers(domain)
        nameservers = result.get("ns", [])

        if not nameservers:
            print_info(f"No nameservers configured for '{domain}'")
            return

        print_success(f"Nameservers for '{domain}':")
        for i, ns in enumerate(nameservers, 1):
            print_info(f"{i}. {ns}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("update-ns")
def update_nameservers(
    domain: str,
    nameservers: list[str] = typer.Argument(..., help="Nameserver hostnames")
):
    """Update nameservers for a domain."""
    client = get_client()

    try:
        result = client.update_nameservers(domain, nameservers)
        print_success(f"Nameservers updated for '{domain}'")

        if "ns" in result:
            print_info("New nameservers:")
            for i, ns in enumerate(result["ns"], 1):
                print_info(f"{i}. {ns}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("auto-renew")
def auto_renew(
    domain: str,
    enable: bool = typer.Option(True, help="Enable (True) or disable (False) auto-renewal")
):
    """Enable or disable auto-renewal for a domain."""
    client = get_client()

    try:
        result = client.update_auto_renew(domain, enable)
        status = "enabled" if enable else "disabled"
        print_success(f"Auto-renewal {status} for '{domain}'")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
