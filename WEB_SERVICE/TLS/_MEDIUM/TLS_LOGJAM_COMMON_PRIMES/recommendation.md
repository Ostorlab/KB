To mitigate LOGJAM common prime attacks:

**Primary Defense - Generate Unique DH Parameters:**

```bash
# Generate unique 2048-bit DH parameters
openssl dhparam -out unique-dhparams.pem 2048

# Apache: use custom parameters
SSLOpenSSLConfCmd DHParameters /path/to/unique-dhparams.pem

# Nginx: specify unique parameters  
ssl_dhparam /path/to/unique-dhparams.pem;
```

**Avoid Default/Common Primes:**

Never use these widely-compromised primes:
- Default Apache 512-bit prime (used by millions of servers)
- Default OpenSSL 512-bit prime (in SSLeay since 1995)
- RFC 5114 standard primes (potentially NSA-influenced)

**Migrate to ECDHE:**

Best solution - eliminate DH vulnerability entirely:
```apache
# Apache: prioritize ECDHE over DHE
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!DHE

# Nginx: use only ECDHE ciphers
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!DHE;
```

**Use Minimum 2048-bit Parameters:**

If DHE is required:
```
# Ensure minimum key size
ssl_dhparam_size 2048;  # Nginx
```

**Testing for Common Primes:**

```bash
# Extract DH parameters from server
openssl s_client -connect example.com:443 -cipher DHE 2>&1 | \
  openssl dhparam -inform PEM -text -noout

# Compare against known vulnerable primes
# Check if prime matches Apache default or other common values
```

**Additional Protections:**

* Use TLS 1.3 which eliminates finite-field DH entirely
* Implement certificate pinning to detect MITM attempts
* Monitor for unusual connection patterns indicating bulk traffic analysis
* Consider Perfect Forward Secrecy implications when choosing cipher suites

**Critical Insight:** Even strong 1024-bit DH parameters become vulnerable when shared across many servers, as the precomputation cost can be amortized. Uniqueness matters as much as size.