To mitigate CRIME attacks:

**Primary Defense - Disable TLS Compression:**

```nginx
# Nginx - TLS compression is disabled by default
# Ensure no explicit compression enabling

# Apache - disable TLS compression
SSLCompression off
```

```python
# Python applications
import ssl
context = ssl.create_default_context()
context.options |= ssl.OP_NO_COMPRESSION
```

**Update Software:**

Most modern browsers and servers have TLS compression disabled by default:
- Chrome/Firefox removed TLS compression support in 2012
- Update to latest OpenSSL versions (1.0.0+ disables by default)
- Use TLS 1.3 which removes compression entirely

**Testing for TLS Compression:**

```bash
# Test if server supports TLS compression
openssl s_client -connect example.com:443 < /dev/null 2>&1 | grep -i compression

# Should show: "Compression: NONE"
# Vulnerable if shows: "Compression: zlib compression"

# Alternative test
nmap --script ssl-enum-ciphers -p 443 example.com
```

**Additional Mitigations:**

* Implement CSRF tokens with random padding to reduce compression efficiency
* Use secure session management with frequent token rotation
* Monitor for unusual request patterns indicating potential attacks
* Enable HSTS to prevent protocol downgrade attempts

Modern applications are generally protected as TLS compression was widely disabled after CRIME disclosure in 2012, but legacy systems may still be vulnerable.