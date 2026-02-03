"""Configuration commands."""

import typer
from rich.prompt import Prompt
from porkbun_cli.config import ConfigManager, Config
from porkbun_cli.utils import print_success, print_error, print_info, print_panel

app = typer.Typer(help="Manage configuration")


@app.command("set")
def set_config(
    apikey: str = typer.Option(None, help="API key"),
    secret: str = typer.Option(None, help="Secret API key"),
    interactive: bool = typer.Option(True, help="Interactive mode")
):
    """Set API credentials."""
    config_manager = ConfigManager()

    if interactive and not apikey:
        print_info("Configure your Porkbun API credentials")
        print_info("Get your credentials at: https://porkbun.com/account/api")
        apikey = Prompt.ask("API Key", password=True)

    if interactive and not secret:
        secret = Prompt.ask("Secret API Key", password=True)

    if not apikey or not secret:
        print_error("Both API key and secret are required")
        raise typer.Exit(1)

    config = Config(apikey=apikey, secretapikey=secret)

    try:
        config_manager.save(config)
        print_success(f"Configuration saved to {config_manager.config_file}")
    except Exception as e:
        print_error(f"Failed to save configuration: {e}")
        raise typer.Exit(1)


@app.command("show")
def show_config():
    """Show current configuration (credentials hidden)."""
    config_manager = ConfigManager()

    try:
        config = config_manager.load()

        if not config.apikey:
            print_info("No configuration found. Run 'porkbun config set' to configure.")
            return

        masked_apikey = f"{config.apikey[:4]}{'*' * (len(config.apikey) - 4)}" if config.apikey else "Not set"
        masked_secret = f"{config.secretapikey[:4]}{'*' * (len(config.secretapikey) - 4)}" if config.secretapikey else "Not set"

        content = f"""API Key: {masked_apikey}
Secret API Key: {masked_secret}
Base URL: {config.base_url}
Config File: {config_manager.config_file}"""

        print_panel(content, "Porkbun Configuration", "green")

    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        raise typer.Exit(1)


@app.command("path")
def show_path():
    """Show configuration file path."""
    config_manager = ConfigManager()
    print_info(f"Configuration file: {config_manager.config_file}")
