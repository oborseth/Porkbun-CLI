"""SSL certificate commands."""

import typer
from pathlib import Path
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import print_success, print_error, print_info, print_panel

app = typer.Typer(help="Manage SSL certificates")


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


@app.command("get")
def get_ssl(
    domain: str,
    save: bool = typer.Option(False, "--save", "-s", help="Save certificates to files"),
    output_dir: Path = typer.Option(Path("."), "--output", "-o", help="Output directory for certificates")
):
    """Retrieve SSL certificate bundle for a domain."""
    client = get_client()

    try:
        result = client.get_ssl_bundle(domain)

        cert_chain = result.get("certificatechain", "")
        private_key = result.get("privatekey", "")
        public_key = result.get("publickey", "")

        if not cert_chain:
            print_error(f"No SSL certificate found for '{domain}'")
            return

        if save:
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save certificate chain
            cert_file = output_dir / f"{domain}.crt"
            with open(cert_file, "w") as f:
                f.write(cert_chain)
            print_success(f"Certificate chain saved to: {cert_file}")

            # Save private key
            if private_key:
                key_file = output_dir / f"{domain}.key"
                with open(key_file, "w") as f:
                    f.write(private_key)
                key_file.chmod(0o600)  # Restrict permissions
                print_success(f"Private key saved to: {key_file}")

            # Save public key
            if public_key:
                pub_file = output_dir / f"{domain}.pub"
                with open(pub_file, "w") as f:
                    f.write(public_key)
                print_success(f"Public key saved to: {pub_file}")

        else:
            # Display certificate info
            print_success(f"SSL Certificate Bundle for '{domain}':")
            print_info(f"\nCertificate Chain ({len(cert_chain)} bytes)")
            print_panel(cert_chain[:500] + "..." if len(cert_chain) > 500 else cert_chain, "Certificate", "green")

            if private_key:
                print_info(f"\nPrivate Key ({len(private_key)} bytes)")
                print_info("Use --save to save the private key to a file")

            if public_key:
                print_info(f"\nPublic Key ({len(public_key)} bytes)")

    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
