To mitigate DROWN attacks:

**Primary Defense - Disable SSLv2 Completely:**

```apache
# Apache - disable SSLv2
SSLProtocol all -SSLv2 -SSLv3
SSLCipherSuite HIGH:!aNULL:!MD5:!SSLv2:!SSLv3
```

```nginx
# Nginx - disable SSLv2 (already disabled by default)
ssl_protocols TLSv1.2 TLSv1.3;
```

**Update OpenSSL:**

Upgrade to patched versions:
- OpenSSL 1.0.2g or later
- OpenSSL 1.0.1s or later
- These versions disable SSLv2 and export ciphers by default

**Check ALL Services Using Same Private Key:**

Critical: Ensure no other services support SSLv2:
```bash
# Check for SSLv2 support across all services
nmap --script ssl-enum-ciphers -p 443,993,995,25,587,465 example.com

# Test specific service for SSLv2
openssl s_client -connect mail.example.com:993 -ssl2
```

**Common vulnerable services:**
- SMTP servers (port 25, 587, 465)
- IMAP servers (port 993)
- POP3 servers (port 995)
- Secondary web servers
- Load balancers and proxies

**Generate New Keys if Needed:**

If you cannot confirm SSLv2 is disabled everywhere:
```bash
# Generate new RSA private key
openssl genrsa -out new-private-key.pem 2048

# Create new certificate signing request
openssl req -new -key new-private-key.pem -out new-csr.pem
```

**Additional Protections:**

* Use ECDHE/DHE cipher suites for perfect forward secrecy
* Implement certificate pinning where possible
* Monitor logs for unusual SSLv2 connection attempts
* Consider network-level filtering of SSLv2 traffic

The key insight: **ANY** service sharing your private key that supports SSLv2 makes **ALL** your TLS services vulnerable, even if they individually disable SSLv2.