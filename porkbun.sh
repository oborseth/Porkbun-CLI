#!/bin/bash
# Convenience wrapper script for Porkbun CLI

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the CLI using Python module
python3 -m porkbun_cli.cli "$@"
