"""DNS management commands."""

from typing import Optional
import typer
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import (
    print_success,
    print_error,
    print_info,
    create_table,
    format_ttl,
    confirm,
    prompt_string,
    prompt_choice,
    console
)

app = typer.Typer(help="Manage DNS records")


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
def list_records(domain: str):
    """List all DNS records for a domain."""
    client = get_client()

    try:
        result = client.list_dns_records(domain)
        records = result.get("records", [])

        if not records:
            print_info(f"No DNS records found for '{domain}'")
            return

        table = create_table(
            f"DNS Records for {domain}",
            ["ID", "Type", "Name", "Content", "TTL", "Priority"]
        )

        for record in records:
            table.add_row(
                record.get("id", "N/A"),
                record.get("type", "N/A"),
                record.get("name", "N/A"),
                record.get("content", "N/A")[:50],  # Truncate long content
                format_ttl(int(record.get("ttl", 0))),
                str(record.get("prio", "")) or "-"
            )

        console.print(table)
        print_success(f"Found {len(records)} record(s)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("get")
def get_record(domain: str, record_id: str):
    """Get a specific DNS record by ID."""
    client = get_client()

    try:
        result = client.get_dns_record(domain, record_id)
        records = result.get("records", [])

        if not records:
            print_error(f"Record '{record_id}' not found")
            return

        record = records[0]
        info = f"""ID: {record.get('id')}
Type: {record.get('type')}
Name: {record.get('name')}
Content: {record.get('content')}
TTL: {format_ttl(int(record.get('ttl', 0)))}
Priority: {record.get('prio', 'N/A')}
Notes: {record.get('notes', 'N/A')}"""

        from porkbun_cli.utils import print_panel
        print_panel(info, f"DNS Record: {record_id}", "green")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("create")
def create_record(
    domain: str,
    record_type: Optional[str] = typer.Option(None, "--type", "-t", help="Record type (A, AAAA, CNAME, MX, etc.)"),
    content: Optional[str] = typer.Option(None, "--content", "-c", help="Record content"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Subdomain name (leave empty for root)"),
    ttl: int = typer.Option(600, "--ttl", help="Time to live in seconds"),
    priority: Optional[int] = typer.Option(None, "--priority", "-p", help="Priority (for MX/SRV records)"),
    notes: Optional[str] = typer.Option(None, "--notes", help="Notes for the record")
):
    """Create a new DNS record."""
    client = get_client()

    # Validate record type
    valid_types = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV", "TLSA", "CAA", "ALIAS", "HTTPS", "SVCB", "SSHFP"]

    # Prompt for record type if not provided
    if record_type is None:
        record_type = prompt_choice(
            "Record type",
            choices=valid_types,
            default="A"
        )

    if record_type.upper() not in valid_types:
        print_error(f"Invalid record type. Valid types: {', '.join(valid_types)}")
        raise typer.Exit(1)

    # Prompt for content if not provided
    if content is None:
        content = prompt_string(f"Record content (e.g., IP address for A record)")

    try:
        result = client.create_dns_record(
            domain=domain,
            record_type=record_type.upper(),
            content=content,
            name=name,
            ttl=ttl,
            prio=priority,
            notes=notes
        )

        record_id = result.get("id")
        print_success(f"DNS record created successfully!")
        if record_id:
            print_info(f"Record ID: {record_id}")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("edit")
def edit_record(
    domain: str,
    record_id: str,
    record_type: Optional[str] = typer.Option(None, "--type", "-t", help="Record type"),
    content: Optional[str] = typer.Option(None, "--content", "-c", help="Record content"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Subdomain name"),
    ttl: int = typer.Option(600, "--ttl", help="Time to live in seconds"),
    priority: Optional[int] = typer.Option(None, "--priority", "-p", help="Priority"),
    notes: Optional[str] = typer.Option(None, "--notes", help="Notes")
):
    """Edit an existing DNS record by ID."""
    client = get_client()

    # Prompt for record type if not provided
    valid_types = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV", "TLSA", "CAA", "ALIAS", "HTTPS", "SVCB", "SSHFP"]
    if record_type is None:
        record_type = prompt_choice("Record type", choices=valid_types, default="A")

    # Prompt for content if not provided
    if content is None:
        content = prompt_string("Record content")

    try:
        result = client.edit_dns_record(
            domain=domain,
            record_id=record_id,
            record_type=record_type.upper(),
            content=content,
            name=name,
            ttl=ttl,
            prio=priority,
            notes=notes
        )

        print_success(f"DNS record '{record_id}' updated successfully!")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("delete")
def delete_record(
    domain: str,
    record_id: str,
    yes: bool = typer.Option(True, "--yes/--no-yes", "-y", help="Skip confirmation (default: yes)")
):
    """Delete a DNS record by ID."""
    client = get_client()

    if not yes:
        if not confirm(f"Delete DNS record '{record_id}' from '{domain}'?", default=False):
            print_info("Deletion cancelled")
            return

    try:
        result = client.delete_dns_record(domain, record_id)
        print_success(f"DNS record '{record_id}' deleted successfully!")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("list-by-type")
def list_by_type(
    domain: str,
    record_type: str = typer.Argument(..., help="Record type (A, AAAA, CNAME, etc.)"),
    subdomain: str = typer.Argument("", help="Subdomain name (empty for root)")
):
    """List DNS records by type and subdomain."""
    client = get_client()

    try:
        result = client.get_dns_records_by_type(domain, record_type.upper(), subdomain)
        records = result.get("records", [])

        if not records:
            print_info(f"No {record_type} records found")
            return

        table = create_table(
            f"{record_type} Records",
            ["ID", "Name", "Content", "TTL", "Priority"]
        )

        for record in records:
            table.add_row(
                record.get("id", "N/A"),
                record.get("name", "N/A"),
                record.get("content", "N/A")[:50],
                format_ttl(int(record.get("ttl", 0))),
                str(record.get("prio", "")) or "-"
            )

        console.print(table)
        print_success(f"Found {len(records)} record(s)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)


@app.command("delete-by-type")
def delete_by_type(
    domain: str,
    record_type: str = typer.Argument(..., help="Record type"),
    subdomain: str = typer.Argument("", help="Subdomain name"),
    yes: bool = typer.Option(True, "--yes/--no-yes", "-y", help="Skip confirmation (default: yes)")
):
    """Delete all DNS records of a specific type and subdomain."""
    client = get_client()

    if not yes:
        if not confirm(
            f"Delete all {record_type} records for '{subdomain or 'root'}' on '{domain}'?",
            default=False
        ):
            print_info("Deletion cancelled")
            return

    try:
        result = client.delete_dns_records_by_type(domain, record_type.upper(), subdomain)
        print_success(f"DNS records deleted successfully!")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
