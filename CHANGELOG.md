# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Shell completions (bash, zsh, fish)
- Batch operations from CSV
- Configuration profiles for multiple accounts
- JSON output mode for scripting
- Interactive REPL mode
- Domain transfer management

## [0.1.0] - 2026-02-03

### Added
- Initial release of Porkbun CLI
- Domain management commands (list, check, create, nameservers, auto-renew)
- DNS record management (full CRUD for all record types)
- URL forwarding support (create, list, delete)
- SSL certificate retrieval
- DNSSEC management
- Glue record management
- Pricing information command
- Configuration management with secure credential storage
- Rich terminal output with tables and colors
- Type-safe API client with full Pydantic validation
- Comprehensive documentation (README, QUICKSTART, EXAMPLES, CONTRIBUTING)
- Unit tests for core functionality
- MIT License

### Features by Category

#### Domain Operations
- List all domains with pagination support
- Check domain availability and pricing
- Register new domains
- Get and update nameservers
- Manage auto-renewal settings

#### DNS Operations
- List all DNS records for a domain
- Get specific DNS record by ID
- Create DNS records (A, AAAA, CNAME, MX, TXT, SRV, TLSA, CAA, ALIAS, HTTPS, SVCB, SSHFP)
- Edit DNS records by ID
- Delete DNS records by ID or by type/name
- Filter records by type and subdomain

#### URL Forwarding
- List URL forwards
- Create redirects (temporary 302 or permanent 301)
- Support for wildcard forwarding
- Include path in forwards

#### SSL & Security
- Retrieve SSL certificate bundles
- Save certificates to files with proper permissions
- DNSSEC record management
- Glue record support for custom nameservers

#### User Experience
- Beautiful Rich terminal output
- Confirmation prompts for destructive operations
- Helpful error messages
- Secure credential storage (0600 permissions)
- Interactive and non-interactive modes
- Comprehensive help for all commands

[Unreleased]: https://github.com/yourusername/porkbun-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/porkbun-cli/releases/tag/v0.1.0
