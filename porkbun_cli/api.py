"""Porkbun API client."""

from typing import Any, Optional
import requests
from requests.exceptions import RequestException


class PorkbunAPIError(Exception):
    """Exception raised for Porkbun API errors."""

    pass


class PorkbunClient:
    """Client for interacting with the Porkbun API."""

    def __init__(
        self,
        apikey: str,
        secretapikey: str,
        base_url: str = "https://api.porkbun.com/api/json/v3"
    ):
        """Initialize Porkbun API client.

        Args:
            apikey: Porkbun API key
            secretapikey: Porkbun secret API key
            base_url: Base URL for API requests
        """
        self.apikey = apikey
        self.secretapikey = secretapikey
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _build_payload(self, **kwargs) -> dict[str, Any]:
        """Build request payload with credentials.

        Args:
            **kwargs: Additional payload parameters

        Returns:
            Dictionary with credentials and additional parameters
        """
        payload = {
            "apikey": self.apikey,
            "secretapikey": self.secretapikey,
        }
        # Filter out None values
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        return payload

    def _request(
        self,
        endpoint: str,
        method: str = "POST",
        payload: Optional[dict] = None,
        require_auth: bool = True
    ) -> dict[str, Any]:
        """Make HTTP request to Porkbun API.

        Args:
            endpoint: API endpoint (without base URL)
            method: HTTP method
            payload: Request payload
            require_auth: Whether to include authentication

        Returns:
            Response data as dictionary

        Raises:
            PorkbunAPIError: If API returns an error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        if require_auth and payload is None:
            payload = self._build_payload()
        elif require_auth and payload is not None:
            payload = self._build_payload(**payload)

        try:
            response = self.session.request(method, url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "ERROR":
                raise PorkbunAPIError(data.get("message", "Unknown error"))

            return data

        except RequestException as e:
            raise PorkbunAPIError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise PorkbunAPIError(f"Invalid JSON response: {str(e)}")

    # System Operations
    def ping(self) -> dict[str, Any]:
        """Test API connectivity and get IP address."""
        return self._request("ping")

    def get_pricing(self) -> dict[str, Any]:
        """Get pricing for all TLDs."""
        return self._request("pricing/get", require_auth=False)

    # Domain Operations
    def list_domains(
        self, start: Optional[int] = None, include_labels: bool = False
    ) -> dict[str, Any]:
        """List all domains in account.

        Args:
            start: Starting position for pagination
            include_labels: Include domain labels in response
        """
        payload = {}
        if start is not None:
            payload["start"] = start
        if include_labels:
            payload["includeLabels"] = "yes"
        return self._request("domain/listAll", payload=payload)

    def check_domain(self, domain: str) -> dict[str, Any]:
        """Check domain availability and pricing."""
        return self._request(f"domain/checkDomain/{domain}")

    def create_domain(self, domain: str, cost: int, agree_to_terms: bool = True) -> dict[str, Any]:
        """Register a new domain.

        Args:
            domain: Domain name to register
            cost: Cost in pennies (for confirmation)
            agree_to_terms: Must be True to proceed
        """
        payload = {"cost": cost, "agreeToTerms": 1 if agree_to_terms else 0}
        return self._request(f"domain/create/{domain}", payload=payload)

    def get_nameservers(self, domain: str) -> dict[str, Any]:
        """Get nameservers for a domain."""
        return self._request(f"domain/getNs/{domain}")

    def update_nameservers(self, domain: str, nameservers: list[str]) -> dict[str, Any]:
        """Update nameservers for a domain.

        Args:
            domain: Domain name
            nameservers: List of nameserver hostnames
        """
        return self._request(f"domain/updateNs/{domain}", payload={"ns": nameservers})

    def update_auto_renew(self, domain: str, status: bool) -> dict[str, Any]:
        """Update auto-renewal status for a domain.

        Args:
            domain: Domain name
            status: True to enable, False to disable
        """
        return self._request(
            f"domain/updateAutoRenew/{domain}",
            payload={"status": "on" if status else "off"}
        )

    # URL Forwarding
    def list_url_forwards(self, domain: str) -> dict[str, Any]:
        """List URL forwards for a domain."""
        return self._request(f"domain/getUrlForwarding/{domain}")

    def add_url_forward(
        self,
        domain: str,
        subdomain: Optional[str],
        location: str,
        forward_type: str = "temporary",
        include_path: bool = False,
        wildcard: bool = False
    ) -> dict[str, Any]:
        """Add URL forward for a domain.

        Args:
            domain: Domain name
            subdomain: Subdomain (None for root)
            location: Target URL
            forward_type: "temporary" (302) or "permanent" (301)
            include_path: Include request path in forward
            wildcard: Enable wildcard forwarding
        """
        payload = {
            "subdomain": subdomain or "",
            "location": location,
            "type": forward_type,
            "includePath": "yes" if include_path else "no",
            "wildcard": "yes" if wildcard else "no"
        }
        return self._request(f"domain/addUrlForward/{domain}", payload=payload)

    def delete_url_forward(self, domain: str, record_id: str) -> dict[str, Any]:
        """Delete URL forward."""
        return self._request(f"domain/deleteUrlForward/{domain}/{record_id}")

    # Glue Records
    def list_glue_records(self, domain: str) -> dict[str, Any]:
        """List glue records for a domain."""
        return self._request(f"domain/getGlue/{domain}")

    def create_glue_record(
        self, domain: str, subdomain: str, ips: list[str]
    ) -> dict[str, Any]:
        """Create glue record.

        Args:
            domain: Domain name
            subdomain: Subdomain for glue record
            ips: List of IP addresses
        """
        return self._request(
            f"domain/createGlue/{domain}/{subdomain}",
            payload={"ips": ips}
        )

    def update_glue_record(
        self, domain: str, subdomain: str, ips: list[str]
    ) -> dict[str, Any]:
        """Update glue record."""
        return self._request(
            f"domain/updateGlue/{domain}/{subdomain}",
            payload={"ips": ips}
        )

    def delete_glue_record(self, domain: str, subdomain: str) -> dict[str, Any]:
        """Delete glue record."""
        return self._request(f"domain/deleteGlue/{domain}/{subdomain}")

    # DNS Records
    def list_dns_records(self, domain: str) -> dict[str, Any]:
        """List all DNS records for a domain."""
        return self._request(f"dns/retrieve/{domain}")

    def get_dns_record(self, domain: str, record_id: str) -> dict[str, Any]:
        """Get specific DNS record by ID."""
        return self._request(f"dns/retrieve/{domain}/{record_id}")

    def get_dns_records_by_type(
        self, domain: str, record_type: str, subdomain: str = ""
    ) -> dict[str, Any]:
        """Get DNS records by type and subdomain."""
        return self._request(f"dns/retrieveByNameType/{domain}/{record_type}/{subdomain}")

    def create_dns_record(
        self,
        domain: str,
        record_type: str,
        content: str,
        name: Optional[str] = None,
        ttl: Optional[int] = None,
        prio: Optional[int] = None,
        notes: Optional[str] = None
    ) -> dict[str, Any]:
        """Create DNS record.

        Args:
            domain: Domain name
            record_type: Record type (A, AAAA, CNAME, MX, etc.)
            content: Record content
            name: Subdomain name (None for root)
            ttl: Time to live in seconds
            prio: Priority (for MX/SRV records)
            notes: Notes for the record
        """
        payload = {
            "type": record_type,
            "content": content,
            "name": name or "",
            "ttl": ttl,
            "prio": prio,
            "notes": notes
        }
        return self._request(f"dns/create/{domain}", payload=payload)

    def edit_dns_record(
        self,
        domain: str,
        record_id: str,
        record_type: str,
        content: str,
        name: Optional[str] = None,
        ttl: Optional[int] = None,
        prio: Optional[int] = None,
        notes: Optional[str] = None
    ) -> dict[str, Any]:
        """Edit DNS record by ID."""
        payload = {
            "type": record_type,
            "content": content,
            "name": name or "",
            "ttl": ttl,
            "prio": prio,
            "notes": notes
        }
        return self._request(f"dns/edit/{domain}/{record_id}", payload=payload)

    def edit_dns_records_by_type(
        self,
        domain: str,
        record_type: str,
        subdomain: str,
        content: str,
        ttl: Optional[int] = None,
        prio: Optional[int] = None,
        notes: Optional[str] = None
    ) -> dict[str, Any]:
        """Edit DNS records by type and subdomain."""
        payload = {
            "content": content,
            "ttl": ttl,
            "prio": prio,
            "notes": notes
        }
        return self._request(
            f"dns/editByNameType/{domain}/{record_type}/{subdomain}",
            payload=payload
        )

    def delete_dns_record(self, domain: str, record_id: str) -> dict[str, Any]:
        """Delete DNS record by ID."""
        return self._request(f"dns/delete/{domain}/{record_id}")

    def delete_dns_records_by_type(
        self, domain: str, record_type: str, subdomain: str = ""
    ) -> dict[str, Any]:
        """Delete DNS records by type and subdomain."""
        return self._request(f"dns/deleteByNameType/{domain}/{record_type}/{subdomain}")

    # DNSSEC
    def list_dnssec_records(self, domain: str) -> dict[str, Any]:
        """List DNSSEC records for a domain."""
        return self._request(f"dns/getDnssecRecords/{domain}")

    def create_dnssec_record(
        self,
        domain: str,
        key_tag: int,
        algorithm: int,
        digest_type: int,
        digest: str,
        **kwargs
    ) -> dict[str, Any]:
        """Create DNSSEC record.

        Args:
            domain: Domain name
            key_tag: Key tag
            algorithm: Algorithm number
            digest_type: Digest type
            digest: Digest value
            **kwargs: Additional optional parameters
        """
        payload = {
            "keyTag": key_tag,
            "alg": algorithm,
            "digestType": digest_type,
            "digest": digest,
            **kwargs
        }
        return self._request(f"dns/createDnssecRecord/{domain}", payload=payload)

    def delete_dnssec_record(self, domain: str, key_tag: int) -> dict[str, Any]:
        """Delete DNSSEC record by key tag."""
        return self._request(f"dns/deleteDnssecRecord/{domain}/{key_tag}")

    # SSL
    def get_ssl_bundle(self, domain: str) -> dict[str, Any]:
        """Get SSL certificate bundle for a domain."""
        return self._request(f"ssl/retrieve/{domain}")
