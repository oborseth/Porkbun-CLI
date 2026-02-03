# Contributing to Porkbun CLI

Thank you for your interest in contributing to Porkbun CLI! This document provides guidelines and instructions for contributing.

## Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd porkbun-cli
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Configure API Credentials

```bash
porkbun config set
```

You'll need valid Porkbun API credentials for testing. Get them at: https://porkbun.com/account/api

## Project Structure

```
porkbun-cli/
├── porkbun_cli/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── api.py              # Porkbun API client
│   ├── config.py           # Configuration management
│   ├── utils.py            # Utility functions
│   └── commands/           # Command modules
│       ├── __init__.py
│       ├── config_cmd.py   # Config commands
│       ├── domain_cmd.py   # Domain management
│       ├── dns_cmd.py      # DNS records
│       ├── ssl_cmd.py      # SSL certificates
│       ├── forward_cmd.py  # URL forwarding
│       ├── glue_cmd.py     # Glue records
│       └── dnssec_cmd.py   # DNSSEC management
├── tests/                  # Test files (to be added)
├── pyproject.toml         # Project metadata
├── README.md
├── EXAMPLES.md
└── CONTRIBUTING.md
```

## Development Workflow

### Running the CLI Locally

Since the package is installed in development mode (`pip install -e .`), you can run:

```bash
porkbun --help
porkbun domain list
```

Any changes you make to the code will be immediately reflected.

### Code Style

We follow PEP 8 style guidelines. Use these tools to maintain code quality:

```bash
# Format code with Black
black porkbun_cli/

# Check types with MyPy
mypy porkbun_cli/

# Lint with Flake8
flake8 porkbun_cli/
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=porkbun_cli
```

## Adding New Features

### Adding a New Command

1. Create a new command module in `porkbun_cli/commands/` (e.g., `new_feature_cmd.py`)

```python
"""New feature commands."""

import typer
from porkbun_cli.api import PorkbunClient, PorkbunAPIError
from porkbun_cli.config import ConfigManager
from porkbun_cli.utils import print_success, print_error

app = typer.Typer(help="Manage new feature")


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


@app.command("list")
def list_items():
    """List items."""
    client = get_client()
    try:
        result = client.some_api_method()
        print_success("Success!")
    except PorkbunAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
```

2. Add the command to `cli.py`:

```python
from porkbun_cli.commands import new_feature_cmd

app.add_typer(new_feature_cmd.app, name="feature")
```

### Adding a New API Method

Add methods to the `PorkbunClient` class in `api.py`:

```python
def new_api_method(self, param: str) -> dict[str, Any]:
    """Description of what this method does.

    Args:
        param: Parameter description

    Returns:
        API response data
    """
    return self._request(f"endpoint/{param}")
```

## Pull Request Process

1. **Fork the repository** and create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes** thoroughly:
   - Run existing tests
   - Add new tests for new features
   - Test manually with the CLI

4. **Update documentation**:
   - Update README.md if needed
   - Add examples to EXAMPLES.md
   - Update docstrings

5. **Commit your changes** with clear commit messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** with:
   - Clear title and description
   - Reference any related issues
   - List of changes made
   - Screenshots (if UI changes)

## Code Review Process

- All submissions require review
- We may suggest changes, improvements, or alternatives
- Make requested changes and push new commits
- Once approved, your PR will be merged

## Guidelines

### General

- Write clear, readable code
- Add comments for complex logic
- Follow existing code patterns
- Keep functions focused and small
- Use type hints

### Error Handling

- Always catch `PorkbunAPIError` in commands
- Provide helpful error messages
- Use appropriate exit codes

### Output

- Use utility functions from `utils.py`:
  - `print_success()` for success messages
  - `print_error()` for errors
  - `print_info()` for information
  - `print_warning()` for warnings
  - `create_table()` for tabular data

### User Experience

- Add helpful help text to commands
- Use clear option names
- Add confirmation prompts for destructive operations
- Support `--yes` flag to skip confirmations
- Show progress for long operations

## Reporting Issues

When reporting issues, please include:

- Your OS and Python version
- Porkbun CLI version (`porkbun --version`)
- Command you ran
- Expected behavior
- Actual behavior
- Error messages (full output)

## Questions?

Feel free to open an issue for:
- Questions about the codebase
- Suggestions for improvements
- Feature requests
- Bug reports

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
