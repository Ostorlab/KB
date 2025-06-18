To mitigate LOGJAM attacks:

**Primary Defense - Disable Export DH Ciphers:**

```apache
# Apache - disable export DH ciphers
SSLCipherSuite HIGH:!aNULL:!MD5:!EXP:!DHE

# Better: use ECDHE instead of DHE
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!DHE
```

```nginx
# Nginx - disable weak DH ciphers
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!DHE:!EXPORT:!DES:!RC4:!MD5;
```

**Use Strong DH Parameters:**

If DHE is required, generate custom 2048-bit+ parameters:
```bash
# Generate strong DH parameters
openssl dhparam -out dhparams.pem 2048

# Apache: use custom DH parameters
SSLOpenSSLConfCmd DHParameters /path/to/dhparams.pem

# Nginx: specify custom DH parameters
ssl_dhparam /path/to/dhparams.pem;
```

**Prefer ECDHE Over DHE:**

ECDHE provides better performance and security:
```
# Prioritize ECDHE cipher suites
ECDHE-ECDSA-AES256-GCM-SHA384
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-ECDSA-CHACHA20-POLY1305
ECDHE-RSA-CHACHA20-POLY1305
```

**Client-Side Protection:**

```java
// Java - disable weak DH
System.setProperty("jdk.tls.disabledAlgorithms", "DH keySize < 1024");
```

**Testing for LOGJAM:**

```bash
# Test for DHE_EXPORT support
nmap --script ssl-enum-ciphers -p 443 example.com | grep DHE_EXPORT

# Should show no DHE_EXPORT ciphers available
openssl s_client -connect example.com:443 -cipher DHE-EXPORT
```

**Additional Mitigations:**

* Use TLS 1.3 which removes support for weak DH parameters
* Implement perfect forward secrecy with ECDHE key exchange
* Monitor for unusual cipher negotiation patterns
* Regularly audit TLS configurations for weak parameters

The fundamental fix is moving away from DHE to ECDHE, which provides equivalent security with better performance and no export-grade vulnerabilities.