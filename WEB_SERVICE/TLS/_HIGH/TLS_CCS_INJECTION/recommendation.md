To mitigate CCS injection attacks:

**Primary Defense - Update OpenSSL:**

Update to patched OpenSSL versions immediately:
- OpenSSL 1.0.1h or later
- OpenSSL 1.0.0m or later  
- OpenSSL 0.9.8za or later

```bash
# Check current version
openssl version

# Update packages
apt-get update && apt-get upgrade openssl  # Debian/Ubuntu
yum update openssl                         # RHEL/CentOS
```

**Restart Services:**

After updating, restart all services using OpenSSL:
```bash
systemctl restart apache2    # or nginx, postfix, etc.
systemctl restart postfix
systemctl restart dovecot
```

**Testing for Vulnerability:**

```bash
# Test server for CCS injection vulnerability
openssl s_client -connect example.com:443 -msg 2>&1 | grep -i "early ccs"

# Use SSL Labs test
curl "https://api.ssllabs.com/api/v3/analyze?host=example.com"
```

**Additional Mitigations:**

* Monitor network traffic for unusual CCS message patterns
* Implement certificate pinning where possible to detect MITM attempts
* Use non-OpenSSL TLS implementations (NSS, GnuTLS) for critical applications
* Enable perfect forward secrecy to limit damage from key compromise

CCS injection does not expose private keys or certificates, so certificate replacement is not required after patching.