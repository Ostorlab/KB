To mitigate BEAST attacks:

**Primary Defense - Upgrade TLS Version:**

```nginx
# Nginx configuration - disable TLS 1.0
ssl_protocols TLSv1.2 TLSv1.3;
# Apache configuration - disable TLS 1.0/SSL 3.0
SSLProtocol -all +TLSv1.2 +TLSv1.3
```

**Alternative Mitigations if TLS 1.0 Required:**

* Use Record Splitting: Enable empty fragment insertion (OpenSSL default)
* Prefer Non-CBC Ciphers: Use stream ciphers or AEAD modes temporarily
* Enable 1/n-1 Record Splitting: Browser-based countermeasure for legacy support

**Testing Commands:**

```bash
# Test for TLS 1.0 support
openssl s_client -connect example.com:443 -tls1

# Check cipher suites
nmap --script ssl-enum-ciphers -p 443 example.com
```

By upgrading to TLS 1.2+ or implementing record splitting countermeasures, organizations can effectively eliminate BEAST attack vectors while maintaining backward compatibility where necessary.