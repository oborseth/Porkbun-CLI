"""DNSSEC management commands."""

import typer
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import (
    print_success,
    print_error,
    print_info,
    create_table,
    confirm,
    console
)

app = typer.Typer(help="Manage DNSSEC records")


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
def list_dnssec(domain: str):
    """List all DNSSEC records for a domain."""
    client = get_client()

    try:
        result = client.list_dnssec_records(domain)
        records = result.get("records", [])

        if not records:
            print_info(f"No DNSSEC records found for '{domain}'")
            return

        table = create_table(
            f"DNSSEC Records for {domain}",
            ["Key Tag", "Algorithm", "Digest Type", "Digest"]
        )

        for record in records:
            table.add_row(
                str(record.get("keyTag", "N/A")),
                str(record.get("alg", "N/A")),
                str(record.get("digestType", "N/A")),
                record.get("digest", "N/A")[:40] + "..."  # Truncate long digest
            )

        console.print(table)
        print_success(f"Found {len(records)} DNSSEC record(s)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("create")
def create_dnssec(
    domain: str,
    key_tag: int = typer.Option(..., "--key-tag", "-k", help="Key tag"),
    algorithm: int = typer.Option(..., "--algorithm", "-a", help="Algorithm number"),
    digest_type: int = typer.Option(..., "--digest-type", "-d", help="Digest type"),
    digest: str = typer.Option(..., "--digest", help="Digest value")
):
    """Create a DNSSEC record."""
    client = get_client()

    try:
        result = client.create_dnssec_record(
            domain=domain,
            key_tag=key_tag,
            algorithm=algorithm,
            digest_type=digest_type,
            digest=digest
        )

        print_success(f"DNSSEC record created for '{domain}'")
        print_info(f"Key Tag: {key_tag}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("delete")
def delete_dnssec(
    domain: str,
    key_tag: int = typer.Argument(..., help="Key tag of the DNSSEC record to delete"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Delete a DNSSEC record by key tag."""
    client = get_client()

    if not yes:
        if not confirm(f"Delete DNSSEC record with key tag '{key_tag}' from '{domain}'?", default=False):
            print_info("Deletion cancelled")
            return

    try:
        result = client.delete_dnssec_record(domain, key_tag)
        print_success(f"DNSSEC record with key tag '{key_tag}' deleted successfully!")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
