# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Considerations

### Credential Storage

API credentials are stored in `~/.porkbun/config.json` with restrictive file permissions (0600 - owner read/write only).

**Important:** Credentials are stored in **plaintext** on disk. This is standard practice for CLI tools (similar to AWS CLI, GitHub CLI, etc.). Ensure your system is secure and encrypted.

### Best Practices

1. **Protect Your Config File**
   - Never commit `~/.porkbun/config.json` to version control
   - Ensure your home directory has appropriate permissions
   - Use full-disk encryption on your system

2. **API Key Security**
   - Treat your Porkbun API credentials like passwords
   - Rotate API keys periodically at https://porkbun.com/account/api
   - Don't share your API keys or config file

3. **SSL Certificates**
   - When using `porkbun ssl get --save`, private keys are saved with 0600 permissions
   - Handle private keys securely and delete them when no longer needed
   - Never commit private keys to version control

4. **Command History**
   - Avoid passing credentials via `--apikey` and `--secret` flags (use interactive mode instead)
   - If you must use flags, prefix commands with a space to avoid shell history on bash/zsh

5. **Multi-User Systems**
   - On shared systems, be aware that root users can access your config file
   - Consider using restricted environments or containers for sensitive operations

## Reporting a Vulnerability

If you discover a security vulnerability, please email:

**security@[your-domain].com**

Or report privately via GitHub Security Advisories:
https://github.com/yourusername/porkbun-cli/security/advisories

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Time

- We will acknowledge your report within 48 hours
- We will provide a detailed response within 7 days
- We will work on a fix and keep you updated on progress

## Security Features

### Current Protections

- ✅ Config file permissions set to 0600 (owner read/write only)
- ✅ Password input hidden during configuration
- ✅ Credentials masked in `config show` output
- ✅ HTTPS-only API communication
- ✅ Request timeouts to prevent hanging
- ✅ No hardcoded credentials
- ✅ No shell injection vulnerabilities
- ✅ SSL certificate verification enabled
- ✅ Confirmation prompts for destructive operations

### Input Validation

The CLI validates user input through:
- Type checking with Pydantic models
- Typer's argument validation
- API-side validation for all operations

### Dependencies

We use well-maintained, security-audited libraries:
- `requests` - HTTP client with security features
- `typer` - CLI framework with safe argument parsing
- `pydantic` - Data validation library
- `rich` - Terminal formatting (no security implications)

Run `pip list` to see exact versions installed.

### Regular Security Updates

- Dependencies are regularly updated to patch vulnerabilities
- CI/CD pipeline includes security checks (coming soon: Dependabot, CodeQL)

## Known Limitations

1. **Plaintext Credential Storage**
   - Credentials are stored in plaintext with file permissions as the only protection
   - This is standard practice for CLI tools but means system compromise = credential compromise
   - Mitigation: Use system encryption, strong system passwords, and regular key rotation

2. **No Built-in Credential Encryption**
   - Unlike browser password managers, the CLI does not encrypt credentials at rest
   - Mitigation: OS-level encryption (FileVault, BitLocker, LUKS) is recommended

3. **Command History**
   - If you pass credentials via flags, they may be stored in shell history
   - Mitigation: Use interactive mode or prefix commands with a space

## Security Checklist for Users

- [ ] Store config file with 0600 permissions (done automatically)
- [ ] Enable full-disk encryption on your system
- [ ] Use strong system passwords
- [ ] Rotate API keys periodically
- [ ] Don't commit config files to version control
- [ ] Review API access logs at Porkbun regularly
- [ ] Use separate API keys for different environments
- [ ] Delete SSL private keys after use
- [ ] Keep the CLI and dependencies updated

## Threat Model

### What We Protect Against

- ✅ Other users on same system reading credentials (via file permissions)
- ✅ Accidental credential exposure in output
- ✅ Command injection attacks
- ✅ Man-in-the-middle attacks (HTTPS)
- ✅ Accidental destructive operations (confirmations)

### What We Don't Protect Against

- ❌ System compromise with root/admin access
- ❌ Physical access to unencrypted disk
- ❌ Malware on the system
- ❌ Keyloggers or screen recorders
- ❌ Compromised dependencies (trust in PyPI ecosystem)

## Compliance Notes

This CLI tool is designed for individual/small team use. If you need:
- SOC 2 compliance
- HIPAA compliance
- PCI DSS compliance
- Enterprise key management

Consider additional security layers like:
- HashiCorp Vault integration
- AWS Secrets Manager
- Environment-based credential injection
- Hardware security modules (HSMs)

## Contact

For security concerns: security@[your-domain].com
For general issues: https://github.com/yourusername/porkbun-cli/issues
