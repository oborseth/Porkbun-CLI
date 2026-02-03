# Porkbun CLI Examples

This document provides practical examples for common use cases with the Porkbun CLI.

## Table of Contents

- [Configuration](#configuration)
- [Domain Management](#domain-management)
- [DNS Records](#dns-records)
- [URL Forwarding](#url-forwarding)
- [SSL Certificates](#ssl-certificates)
- [Advanced Usage](#advanced-usage)

## Configuration

### Initial Setup

```bash
# Interactive configuration
porkbun config set

# Or set credentials directly
porkbun config set --apikey your_api_key --secret your_secret_key
```

### View Current Configuration

```bash
# Show configuration (credentials masked)
porkbun config show

# Show config file location
porkbun config path
```

### Test Connectivity

```bash
# Ping the API and check your IP
porkbun ping
```

## Domain Management

### List All Domains

```bash
# List all domains
porkbun domain list

# Include domain labels
porkbun domain list --include-labels

# Paginate results (starting from position 1000)
porkbun domain list --start 1000
```

### Check Domain Availability

```bash
# Check if a domain is available
porkbun domain check example.com

# Check multiple domains
porkbun domain check awesome-domain.dev
porkbun domain check my-new-site.io
```

### Register a Domain

```bash
# Check the price first
porkbun domain check example.com
# Output: Registration: $8.99 (899 pennies)

# Register the domain (899 pennies = $8.99)
porkbun domain create example.com --cost 899

# Skip confirmation prompt
porkbun domain create example.com --cost 899 --yes
```

### Manage Nameservers

```bash
# Get current nameservers
porkbun domain get-ns example.com

# Update nameservers
porkbun domain update-ns example.com ns1.example.com ns2.example.com

# Use Cloudflare nameservers
porkbun domain update-ns example.com \
  dane.ns.cloudflare.com \
  ivy.ns.cloudflare.com
```

### Auto-Renewal

```bash
# Enable auto-renewal
porkbun domain auto-renew example.com --enable

# Disable auto-renewal
porkbun domain auto-renew example.com --no-enable
```

## DNS Records

### List DNS Records

```bash
# List all records for a domain
porkbun dns list example.com

# List specific record type
porkbun dns list-by-type example.com A

# List records for a subdomain
porkbun dns list-by-type example.com A www
```

### Create DNS Records

#### A Record (IPv4)

```bash
# Create A record for root domain
porkbun dns create example.com \
  --type A \
  --content 192.0.2.1 \
  --ttl 600

# Create A record for subdomain
porkbun dns create example.com \
  --type A \
  --name www \
  --content 192.0.2.1 \
  --ttl 600
```

#### AAAA Record (IPv6)

```bash
# Create AAAA record
porkbun dns create example.com \
  --type AAAA \
  --name www \
  --content 2001:0db8:85a3:0000:0000:8a2e:0370:7334 \
  --ttl 600
```

#### CNAME Record

```bash
# Create CNAME record
porkbun dns create example.com \
  --type CNAME \
  --name blog \
  --content example.com \
  --ttl 600
```

#### MX Record

```bash
# Create MX record with priority
porkbun dns create example.com \
  --type MX \
  --content mail.example.com \
  --priority 10 \
  --ttl 3600
```

#### TXT Record

```bash
# Create TXT record (SPF)
porkbun dns create example.com \
  --type TXT \
  --content "v=spf1 include:_spf.google.com ~all" \
  --ttl 3600

# Create TXT record for subdomain (DKIM)
porkbun dns create example.com \
  --type TXT \
  --name google._domainkey \
  --content "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3..." \
  --ttl 3600
```

#### SRV Record

```bash
# Create SRV record for service
porkbun dns create example.com \
  --type SRV \
  --name _service._tcp \
  --content "10 5060 server.example.com" \
  --priority 10 \
  --ttl 3600
```

### View DNS Records

```bash
# Get specific record by ID
porkbun dns get example.com 123456789

# View all A records
porkbun dns list-by-type example.com A
```

### Edit DNS Records

```bash
# Edit a specific record by ID
porkbun dns edit example.com 123456789 \
  --type A \
  --content 192.0.2.2 \
  --name www \
  --ttl 600

# Edit with notes
porkbun dns edit example.com 123456789 \
  --type A \
  --content 192.0.2.2 \
  --name www \
  --ttl 600 \
  --notes "Updated production IP"
```

### Delete DNS Records

```bash
# Delete specific record by ID
porkbun dns delete example.com 123456789

# Delete without confirmation
porkbun dns delete example.com 123456789 --yes

# Delete all records of a type
porkbun dns delete-by-type example.com A www --yes
```

## URL Forwarding

### List URL Forwards

```bash
# List all forwards for a domain
porkbun forward list example.com
```

### Create URL Forwards

```bash
# Temporary redirect (302) from www to root
porkbun forward add example.com \
  --subdomain www \
  --location https://example.com \
  --type temporary

# Permanent redirect (301)
porkbun forward add example.com \
  --subdomain www \
  --location https://example.com \
  --type permanent

# Forward with path preservation
porkbun forward add example.com \
  --subdomain blog \
  --location https://medium.com/@yourname \
  --type permanent \
  --include-path

# Wildcard forwarding
porkbun forward add example.com \
  --subdomain "*" \
  --location https://example.com \
  --type permanent \
  --wildcard
```

### Delete URL Forwards

```bash
# Delete a specific forward
porkbun forward delete example.com 123456 --yes
```

## SSL Certificates

### Retrieve SSL Certificates

```bash
# View certificate info
porkbun ssl get example.com

# Save certificates to files
porkbun ssl get example.com --save

# Save to specific directory
porkbun ssl get example.com --save --output ./certs/
```

The saved files will be:
- `example.com.crt` - Certificate chain
- `example.com.key` - Private key (permissions set to 600)
- `example.com.pub` - Public key

## Advanced Usage

### DNSSEC Management

```bash
# List DNSSEC records
porkbun dnssec list example.com

# Create DNSSEC record
porkbun dnssec create example.com \
  --key-tag 12345 \
  --algorithm 8 \
  --digest-type 2 \
  --digest "1234567890ABCDEF..."

# Delete DNSSEC record
porkbun dnssec delete example.com 12345 --yes
```

### Glue Records

```bash
# List glue records
porkbun glue list example.com

# Create glue record
porkbun glue create example.com ns1 \
  --ip 192.0.2.1 \
  --ip 2001:db8::1

# Update glue record
porkbun glue update example.com ns1 \
  --ip 192.0.2.2

# Delete glue record
porkbun glue delete example.com ns1 --yes
```

### View Pricing

```bash
# Show all TLD pricing
porkbun pricing

# Search for specific TLD
porkbun pricing --search dev

# Increase results limit
porkbun pricing --limit 100
```

## Common Workflows

### Setting Up a New Website

```bash
# 1. Check domain availability
porkbun domain check mysite.com

# 2. Register the domain (if available)
porkbun domain create mysite.com --cost 899

# 3. Create A record for root domain
porkbun dns create mysite.com \
  --type A \
  --content 192.0.2.1 \
  --ttl 600

# 4. Create A record for www
porkbun dns create mysite.com \
  --type A \
  --name www \
  --content 192.0.2.1 \
  --ttl 600

# 5. Add email (MX) records
porkbun dns create mysite.com \
  --type MX \
  --content mail.mysite.com \
  --priority 10 \
  --ttl 3600
```

### Migrating to a New Server

```bash
# 1. List current DNS records
porkbun dns list example.com

# 2. Update A record to new IP
porkbun dns edit example.com 123456789 \
  --type A \
  --content 198.51.100.1 \
  --ttl 300

# 3. Lower TTL for faster propagation initially
# (Wait for DNS to propagate)

# 4. Later, increase TTL back to normal
porkbun dns edit example.com 123456789 \
  --type A \
  --content 198.51.100.1 \
  --ttl 3600
```

### Setting Up Email with Google Workspace

```bash
# Add MX records
for priority in 1 5 5 10 10; do
  porkbun dns create example.com \
    --type MX \
    --content "aspmx${priority}.googlemail.com" \
    --priority ${priority} \
    --ttl 3600
done

# Add SPF record
porkbun dns create example.com \
  --type TXT \
  --content "v=spf1 include:_spf.google.com ~all" \
  --ttl 3600

# Verify domain ownership
porkbun dns create example.com \
  --type TXT \
  --content "google-site-verification=YOUR_VERIFICATION_CODE" \
  --ttl 3600
```

## Tips and Best Practices

1. **Always check before registering**: Use `porkbun domain check` to verify pricing
2. **Lower TTL before changes**: Set TTL to 300 (5 minutes) before IP changes
3. **Test with ping**: Use `porkbun ping` to verify API connectivity
4. **Use --yes flag carefully**: Only use in scripts when you're sure
5. **Backup DNS records**: Run `porkbun dns list domain.com` and save output before major changes
6. **Use descriptive notes**: Add notes to DNS records for documentation
7. **Secure your config**: Config file is stored at `~/.porkbun/config.json` with restricted permissions
