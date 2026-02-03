# Porkbun CLI - Project Summary

A professional command-line interface for managing domains and DNS records through the Porkbun API, built with modern Python tools and best practices.

## Overview

**Porkbun CLI** provides a comprehensive, user-friendly interface to interact with all Porkbun API endpoints. It features beautiful terminal output, robust error handling, secure credential storage, and an intuitive command structure.

## Key Features

### Core Functionality

- **Domain Management**: List, check availability, register, manage nameservers, and control auto-renewal
- **DNS Records**: Full CRUD operations for all DNS record types (A, AAAA, CNAME, MX, TXT, SRV, etc.)
- **URL Forwarding**: Create and manage HTTP redirects (301/302)
- **SSL Certificates**: Retrieve and save SSL certificate bundles
- **DNSSEC**: Manage DNSSEC records for enhanced security
- **Glue Records**: Create and manage nameserver glue records
- **Pricing**: View current pricing for all TLDs

### Technical Features

- **Beautiful Output**: Rich terminal formatting with tables, colors, and panels
- **Secure Configuration**: Credentials stored with restricted file permissions (0600)
- **Type Safety**: Full type hints using Pydantic models
- **Error Handling**: Comprehensive error handling with helpful messages
- **Confirmation Prompts**: Safety prompts for destructive operations
- **Flexible Input**: Support for both interactive and non-interactive modes

## Architecture

### Technology Stack

- **Typer**: Modern CLI framework with excellent type support
- **Rich**: Beautiful terminal output with tables and colors
- **Requests**: HTTP client for API communication
- **Pydantic**: Data validation and settings management
- **Python 3.8+**: Modern Python with type hints

### Project Structure

```
porkbun-cli/
├── porkbun_cli/                    # Main package
│   ├── __init__.py                 # Package initialization
│   ├── cli.py                      # Main CLI entry point
│   ├── api.py                      # Porkbun API client
│   ├── config.py                   # Configuration management
│   ├── utils.py                    # Utility functions
│   └── commands/                   # Command modules
│       ├── __init__.py
│       ├── config_cmd.py           # Configuration commands
│       ├── domain_cmd.py           # Domain management
│       ├── dns_cmd.py              # DNS record operations
│       ├── ssl_cmd.py              # SSL certificate retrieval
│       ├── forward_cmd.py          # URL forwarding
│       ├── glue_cmd.py             # Glue record management
│       └── dnssec_cmd.py           # DNSSEC operations
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_config.py              # Configuration tests
│   └── test_api.py                 # API client tests
├── docs/                           # Documentation
│   ├── README.md                   # Main documentation
│   ├── QUICKSTART.md               # Quick start guide
│   ├── EXAMPLES.md                 # Usage examples
│   └── CONTRIBUTING.md             # Contribution guidelines
├── pyproject.toml                  # Project metadata & dependencies
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── porkbun.sh                      # Convenience wrapper script
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore rules
```

## Command Structure

### Main Commands

```
porkbun
├── ping                            # Test API connectivity
├── pricing                         # View TLD pricing
├── config
│   ├── set                         # Set API credentials
│   ├── show                        # Show current config
│   └── path                        # Show config file path
├── domain
│   ├── list                        # List all domains
│   ├── check                       # Check availability
│   ├── create                      # Register domain
│   ├── get-ns                      # Get nameservers
│   ├── update-ns                   # Update nameservers
│   └── auto-renew                  # Manage auto-renewal
├── dns
│   ├── list                        # List all DNS records
│   ├── get                         # Get specific record
│   ├── create                      # Create DNS record
│   ├── edit                        # Edit DNS record
│   ├── delete                      # Delete DNS record
│   ├── list-by-type                # Filter by type
│   └── delete-by-type              # Bulk delete
├── forward
│   ├── list                        # List URL forwards
│   ├── add                         # Add URL forward
│   └── delete                      # Delete forward
├── ssl
│   └── get                         # Get SSL certificate
├── glue
│   ├── list                        # List glue records
│   ├── create                      # Create glue record
│   ├── update                      # Update glue record
│   └── delete                      # Delete glue record
└── dnssec
    ├── list                        # List DNSSEC records
    ├── create                      # Create DNSSEC record
    └── delete                      # Delete DNSSEC record
```

## API Client Design

### PorkbunClient Class

The `PorkbunClient` class in `api.py` provides:

- **Automatic Authentication**: Credentials injected into all requests
- **Error Handling**: Converts API errors to `PorkbunAPIError` exceptions
- **Type Safety**: Full type hints for all methods
- **Session Management**: Persistent HTTP session for performance
- **Flexible Configuration**: Customizable base URL

### Key Methods

- Domain operations: `list_domains()`, `check_domain()`, `create_domain()`
- DNS operations: `list_dns_records()`, `create_dns_record()`, `delete_dns_record()`
- URL forwarding: `list_url_forwards()`, `add_url_forward()`
- SSL: `get_ssl_bundle()`
- DNSSEC: `list_dnssec_records()`, `create_dnssec_record()`
- Glue records: `list_glue_records()`, `create_glue_record()`

## Configuration Management

### Secure Storage

- Location: `~/.porkbun/config.json`
- Permissions: 0600 (read/write for owner only)
- Format: JSON with Pydantic validation

### Config Schema

```json
{
  "apikey": "pk_xxxxxxxxxxxx",
  "secretapikey": "sk_xxxxxxxxxxxx",
  "base_url": "https://api.porkbun.com/api/json/v3"
}
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest
pytest --cov=porkbun_cli  # With coverage
```

### Code Quality

```bash
black porkbun_cli/         # Format code
mypy porkbun_cli/          # Type checking
flake8 porkbun_cli/        # Linting
```

## Usage Examples

### Basic Workflow

```bash
# Configure credentials
python3 -m porkbun_cli.cli config set

# Test connection
python3 -m porkbun_cli.cli ping

# List domains
python3 -m porkbun_cli.cli domain list

# Create DNS record
python3 -m porkbun_cli.cli dns create example.com \
  --type A --name www --content 192.0.2.1 --ttl 600
```

### Advanced Usage

See [EXAMPLES.md](EXAMPLES.md) for comprehensive examples covering:
- Domain registration workflows
- DNS record management patterns
- URL forwarding configurations
- SSL certificate retrieval
- Server migration procedures
- Email provider setup (Google Workspace, etc.)

## Comparison to Other Tools

### vs. Web Interface
- **Faster**: Command-line is quicker for bulk operations
- **Scriptable**: Integrate into automation workflows
- **Version Controllable**: Configuration as code

### vs. Direct API Calls
- **Easier**: No need to handle authentication, formatting
- **Validated**: Input validation and helpful error messages
- **Documented**: Built-in help for all commands

### Inspired by Claude Code
- **User Experience**: Clean, helpful output like Claude Code
- **Error Handling**: Clear error messages
- **Documentation**: Comprehensive guides and examples
- **Modern Stack**: Using best practices and current tools

## Future Enhancements

Potential additions:
- Batch operations (bulk DNS updates from CSV)
- Configuration profiles (multiple accounts)
- Shell completions (bash, zsh, fish)
- Export/import DNS zones
- Domain transfer management
- Monitoring and alerts
- Interactive mode (REPL)
- JSON output mode for scripting

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Resources

- **API Documentation**: https://porkbun.com/api/json/v3/documentation
- **Swagger Spec**: https://porkbun.com/openapi/swagger.json
- **Porkbun Support**: support@porkbun.com

## Credits

Built with modern Python tools and inspired by the excellent UX of Claude Code CLI.

---

**Version**: 0.1.0
**Python**: 3.8+
**License**: MIT
**Status**: Production Ready
