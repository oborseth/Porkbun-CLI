# Porkbun CLI - Quick Start Guide

Get up and running with Porkbun CLI in minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Porkbun account with API access enabled

## Installation

### Option 1: Install from Source (Development)

```bash
# Clone or navigate to the repository
cd porkbun-cli

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Option 2: Install from PyPI (When Published)

```bash
pip install porkbun-cli
```

## Initial Configuration

### Step 1: Get Your API Credentials

1. Log in to your Porkbun account
2. Go to https://porkbun.com/account/api
3. Enable API access for your account
4. Copy your API Key and Secret API Key

### Step 2: Configure the CLI

Run the configuration command:

```bash
python3 -m porkbun_cli.cli config set
```

Or if the `porkbun` command is in your PATH:

```bash
porkbun config set
```

Enter your credentials when prompted:
- API Key: `pk_xxxxxxxxxxxxx`
- Secret API Key: `sk_xxxxxxxxxxxxx`

Your credentials will be securely stored in `~/.porkbun/config.json` with restricted file permissions.

### Step 3: Test Your Connection

```bash
python3 -m porkbun_cli.cli ping
```

You should see:
```
✓ API connection successful!
ℹ Your IP address: x.x.x.x
```

## Common Tasks

### List Your Domains

```bash
python3 -m porkbun_cli.cli domain list
```

### Check Domain Availability

```bash
python3 -m porkbun_cli.cli domain check example.com
```

### List DNS Records

```bash
python3 -m porkbun_cli.cli dns list example.com
```

### Create a DNS Record

```bash
# Create an A record for www subdomain
python3 -m porkbun_cli.cli dns create example.com \
  --type A \
  --name www \
  --content 192.0.2.1 \
  --ttl 600
```

### View Pricing

```bash
# Show all TLD pricing
python3 -m porkbun_cli.cli pricing

# Search for specific TLD
python3 -m porkbun_cli.cli pricing --search dev
```

## Shell Alias (Optional)

To make it easier to use, add this to your `~/.bashrc` or `~/.zshrc`:

```bash
alias porkbun='python3 -m porkbun_cli.cli'
```

Then reload your shell:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use:

```bash
porkbun domain list
porkbun dns create example.com --type A --name www --content 192.0.2.1
```

## Getting Help

### General Help

```bash
python3 -m porkbun_cli.cli --help
```

### Command-Specific Help

```bash
python3 -m porkbun_cli.cli domain --help
python3 -m porkbun_cli.cli dns create --help
```

### Documentation

- Full documentation: See [README.md](README.md)
- Examples: See [EXAMPLES.md](EXAMPLES.md)
- API Reference: https://porkbun.com/api/json/v3/documentation

## Troubleshooting

### Command Not Found

If you get "command not found" after installation:

1. Make sure you activated your virtual environment (if using one)
2. Use the full Python module syntax: `python3 -m porkbun_cli.cli`
3. Or create a shell alias as shown above

### API Credentials Error

If you see "API credentials not configured":

1. Run `python3 -m porkbun_cli.cli config set` to configure
2. Verify your credentials at https://porkbun.com/account/api
3. Check that API access is enabled for your account

### Connection Error

If you can't connect to the API:

1. Check your internet connection
2. Verify your credentials are correct
3. Ensure API access is enabled in your Porkbun account
4. Try the ping command: `python3 -m porkbun_cli.cli ping`

## Next Steps

- Read [EXAMPLES.md](EXAMPLES.md) for comprehensive usage examples
- Explore all available commands with `--help`
- Set up domain automation scripts
- Integrate with your deployment workflows

## Support

- Issues: Report bugs and feature requests on GitHub
- API Documentation: https://porkbun.com/api/json/v3/documentation
- Porkbun Support: support@porkbun.com

Happy domain managing!
