"""Configuration management for Porkbun CLI."""

import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration model for Porkbun API credentials."""

    apikey: Optional[str] = Field(None, description="Porkbun API key")
    secretapikey: Optional[str] = Field(None, description="Porkbun secret API key")
    base_url: str = Field(
        "https://api.porkbun.com/api/json/v3",
        description="Base URL for Porkbun API"
    )


class ConfigManager:
    """Manages configuration file for Porkbun CLI."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager.

        Args:
            config_dir: Directory to store config file. Defaults to ~/.porkbun
        """
        self.config_dir = config_dir or Path.home() / ".porkbun"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> Config:
        """Load configuration from file.

        Returns:
            Config object with loaded settings
        """
        if not self.config_file.exists():
            return Config()

        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
            return Config(**data)
        except Exception as e:
            raise ValueError(f"Failed to load config: {e}")

    def save(self, config: Config) -> None:
        """Save configuration to file.

        Args:
            config: Config object to save
        """
        with open(self.config_file, "w") as f:
            json.dump(config.model_dump(), f, indent=2)

        # Set restrictive permissions on config file
        self.config_file.chmod(0o600)

    def get_credentials(self) -> tuple[str, str]:
        """Get API credentials from config.

        Returns:
            Tuple of (apikey, secretapikey)

        Raises:
            ValueError: If credentials are not configured
        """
        config = self.load()
        if not config.apikey or not config.secretapikey:
            raise ValueError(
                "API credentials not configured. Run 'porkbun config set' to configure."
            )
        return config.apikey, config.secretapikey
