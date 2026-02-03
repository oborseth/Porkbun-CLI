"""Tests for API client."""

import pytest
from porkbun_cli.api import PorkbunClient, PorkbunAPIError


def test_client_initialization():
    """Test client initialization."""
    client = PorkbunClient(
        apikey="test_key",
        secretapikey="test_secret"
    )

    assert client.apikey == "test_key"
    assert client.secretapikey == "test_secret"
    assert "porkbun.com" in client.base_url


def test_build_payload():
    """Test payload building with credentials."""
    client = PorkbunClient(
        apikey="test_key",
        secretapikey="test_secret"
    )

    payload = client._build_payload(test_param="value")

    assert payload["apikey"] == "test_key"
    assert payload["secretapikey"] == "test_secret"
    assert payload["test_param"] == "value"


def test_build_payload_filters_none():
    """Test that None values are filtered from payload."""
    client = PorkbunClient(
        apikey="test_key",
        secretapikey="test_secret"
    )

    payload = client._build_payload(test_param="value", none_param=None)

    assert "test_param" in payload
    assert "none_param" not in payload


# Note: Actual API calls would require mocking or integration tests
# with real credentials. These are basic unit tests for the structure.


def test_base_url_trailing_slash():
    """Test that base URL trailing slash is handled."""
    client = PorkbunClient(
        apikey="test",
        secretapikey="test",
        base_url="https://api.example.com/"
    )

    assert not client.base_url.endswith("/")
