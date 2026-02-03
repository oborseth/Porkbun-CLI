"""Tests for configuration management."""

import pytest
from pathlib import Path
from porkbun_cli.config import Config, ConfigManager


def test_config_model():
    """Test Config model creation."""
    config = Config(apikey="test_key", secretapikey="test_secret")
    assert config.apikey == "test_key"
    assert config.secretapikey == "test_secret"
    assert "porkbun.com" in config.base_url


def test_config_manager_init(tmp_path):
    """Test ConfigManager initialization."""
    manager = ConfigManager(config_dir=tmp_path)
    assert manager.config_dir == tmp_path
    assert manager.config_file == tmp_path / "config.json"


def test_config_save_and_load(tmp_path):
    """Test saving and loading configuration."""
    manager = ConfigManager(config_dir=tmp_path)

    # Create and save config
    config = Config(apikey="test_key", secretapikey="test_secret")
    manager.save(config)

    # Verify file exists
    assert manager.config_file.exists()

    # Load and verify
    loaded_config = manager.load()
    assert loaded_config.apikey == "test_key"
    assert loaded_config.secretapikey == "test_secret"


def test_get_credentials_without_config(tmp_path):
    """Test getting credentials when not configured."""
    manager = ConfigManager(config_dir=tmp_path)

    with pytest.raises(ValueError, match="not configured"):
        manager.get_credentials()


def test_get_credentials_with_config(tmp_path):
    """Test getting credentials when configured."""
    manager = ConfigManager(config_dir=tmp_path)

    # Save config
    config = Config(apikey="test_key", secretapikey="test_secret")
    manager.save(config)

    # Get credentials
    apikey, secret = manager.get_credentials()
    assert apikey == "test_key"
    assert secret == "test_secret"


def test_config_file_permissions(tmp_path):
    """Test that config file has restrictive permissions."""
    manager = ConfigManager(config_dir=tmp_path)

    config = Config(apikey="test_key", secretapikey="test_secret")
    manager.save(config)

    # Check file permissions (0o600 = read/write for owner only)
    import stat
    file_stat = manager.config_file.stat()
    assert stat.S_IMODE(file_stat.st_mode) == 0o600
