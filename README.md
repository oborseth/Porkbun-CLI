# Porkbun CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful, user-friendly command-line interface for managing domains and DNS records through the [Porkbun API](https://porkbun.com/api/json/v3/documentation).

## ✨ Features

- 🌐 **Domain Management** - List, register, check availability, manage nameservers
- 📝 **DNS Records** - Full CRUD operations for all DNS record types (A, AAAA, CNAME, MX, TXT, SRV, etc.)
- 🔀 **URL Forwarding** - Configure HTTP redirects (301/302) with wildcard support
- 🔒 **SSL Certificates** - Retrieve and save SSL certificate bundles
- 🛡️ **DNSSEC** - Manage DNSSEC records for enhanced security
- 🔗 **Glue Records** - Create and manage nameserver glue records
- 💰 **Pricing** - View current pricing for all TLDs
- 🎨 **Beautiful Output** - Rich terminal formatting with tables, colors, and panels
- 🔐 **Secure Configuration** - API credentials stored with restricted file permissions
- ⚡ **Type Safe** - Full type hints and validation with Pydantic
- 🚀 **Easy to Use** - Intuitive command structure with helpful error messages

## 📦 Installation

### From Source (Development)

```bash
git clone https://github.com/yourusername/porkbun-cli.git
cd porkbun-cli

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install porkbun-cli
```

## 🚀 Quick Start

### 1. Get API Credentials

1. Log in to [Porkbun](https://porkbun.com)
2. Go to [API Access](https://porkbun.com/account/api)
3. Enable API access and copy your credentials

### 2. Configure CLI

```bash
porkbun config set
# Or: python3 -m porkbun_cli.cli config set
```

Enter your API key and secret when prompted. Your credentials will be securely stored in `~/.porkbun/config.json`.

### 3. Test Connection

```bash
porkbun ping
```

You should see: `✓ API connection successful!`

### 4. Start Managing Domains

```bash
# List your domains
porkbun domain list

# Check domain availability
porkbun domain check awesome-domain.com

# List DNS records
porkbun dns list example.com

# Create a DNS record
porkbun dns create example.com --type A --name www --content 192.0.2.1 --ttl 600

# View pricing
porkbun pricing --search dev
```

## 📖 Usage

### Domain Management

```bash
# List all domains
porkbun domain list

# Check if domain is available
porkbun domain check example.com

# Register a domain (899 pennies = $8.99)
porkbun domain create example.com --cost 899

# Get nameservers
porkbun domain get-ns example.com

# Update nameservers
porkbun domain update-ns example.com ns1.example.com ns2.example.com

# Enable auto-renewal
porkbun domain auto-renew example.com --enable
```

### DNS Management

```bash
# List all DNS records
porkbun dns list example.com

# Create A record
porkbun dns create example.com \
  --type A \
  --name www \
  --content 192.0.2.1 \
  --ttl 600

# Create MX record
porkbun dns create example.com \
  --type MX \
  --content mail.example.com \
  --priority 10

# Edit record
porkbun dns edit example.com RECORD_ID \
  --type A \
  --content 192.0.2.2

# Delete record
porkbun dns delete example.com RECORD_ID --yes

# List records by type
porkbun dns list-by-type example.com A www
```

### URL Forwarding

```bash
# List forwards
porkbun forward list example.com

# Add permanent redirect (301)
porkbun forward add example.com \
  --subdomain www \
  --location https://example.com \
  --type permanent

# Add with wildcard
porkbun forward add example.com \
  --location https://example.com \
  --type permanent \
  --wildcard

# Delete forward
porkbun forward delete example.com FORWARD_ID
```

### SSL Certificates

```bash
# View certificate
porkbun ssl get example.com

# Save to files
porkbun ssl get example.com --save --output ./certs/
```

### Additional Commands

See full documentation:
- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Examples](EXAMPLES.md) - Comprehensive usage examples and workflows
- [Contributing](CONTRIBUTING.md) - Development guide

## 🎨 Command Structure

```
porkbun
├── ping              # Test API connectivity
├── pricing           # View TLD pricing
├── config            # Manage configuration
│   ├── set          # Set credentials
│   ├── show         # Show config (masked)
│   └── path         # Show config file path
├── domain            # Domain management
│   ├── list         # List domains
│   ├── check        # Check availability
│   ├── create       # Register domain
│   ├── get-ns       # Get nameservers
│   ├── update-ns    # Update nameservers
│   └── auto-renew   # Manage auto-renewal
├── dns               # DNS records
│   ├── list         # List all records
│   ├── get          # Get specific record
│   ├── create       # Create record
│   ├── edit         # Edit record
│   ├── delete       # Delete record
│   ├── list-by-type # Filter by type
│   └── delete-by-type
├── forward           # URL forwarding
│   ├── list
│   ├── add
│   └── delete
├── ssl               # SSL certificates
│   └── get
├── glue              # Glue records
│   ├── list
│   ├── create
│   ├── update
│   └── delete
└── dnssec            # DNSSEC
    ├── list
    ├── create
    └── delete
```

## 🔧 Configuration

Configuration is stored in `~/.porkbun/config.json` with restricted permissions (0600).

```bash
# Set credentials interactively
porkbun config set

# Set credentials directly
porkbun config set --apikey pk_xxx --secret sk_xxx

# View configuration (credentials masked)
porkbun config show

# Show config file path
porkbun config path
```

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/porkbun-cli.git
cd porkbun-cli

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=porkbun_cli

# Type checking
mypy porkbun_cli/

# Linting
flake8 porkbun_cli/

# Format code
black porkbun_cli/
```

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Examples](EXAMPLES.md)** - Real-world usage examples and workflows
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Project Summary](PROJECT_SUMMARY.md)** - Technical architecture overview
- **[API Documentation](https://porkbun.com/api/json/v3/documentation)** - Official Porkbun API docs

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/)
- Inspired by the excellent UX of [Claude Code](https://claude.com/claude-code)
- Powered by the [Porkbun API](https://porkbun.com/api/json/v3/documentation)

## 📧 Support

- 🐛 Report bugs via [GitHub Issues](https://github.com/yourusername/porkbun-cli/issues)
- 💡 Request features via [GitHub Issues](https://github.com/yourusername/porkbun-cli/issues)
- 📖 Read the [documentation](QUICKSTART.md)
- 🌐 Visit [Porkbun Support](https://porkbun.com/support)

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for the domain management community**
