To mitigate FREAK attacks:

**Primary Defense - Disable Export Cipher Suites:**

```apache
# Apache - disable export-grade ciphers
SSLCipherSuite HIGH:!aNULL:!MD5:!EXP:!RC4

# More secure configuration
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!EXP
```

```nginx
# Nginx - disable export ciphers
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA;
```

**Update TLS Libraries:**

Ensure all TLS implementations are patched:
- OpenSSL 1.0.1k+ (CVE-2015-0204 fixed)
- Update mobile apps using vulnerable libraries
- Patch embedded systems and IoT devices

**Testing for FREAK Vulnerability:**

```bash
# Test server for export cipher support
openssl s_client -connect example.com:443 -cipher EXPORT

# Should fail with "no cipher match" if properly configured
# Test with SSL Labs
curl "https://api.ssllabs.com/api/v3/analyze?host=example.com"
```

**Client-Side Protection:**

```python
# Python - disable export ciphers
import ssl
context = ssl.create_default_context()
context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS:!EXPORT')
```

**Additional Mitigations:**

* Use TLS 1.3 which completely removes export cipher support
* Implement perfect forward secrecy (PFS) with ECDHE/DHE key exchange
* Regularly audit cipher suite configurations for weak algorithms
* Monitor for unusual TLS negotiation patterns indicating downgrade attempts

Modern browsers and servers have disabled export ciphers by default, but legacy systems and embedded devices may still be vulnerable.