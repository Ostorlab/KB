To mitigate SWEET32 attacks:

**Primary Defense - Disable 64-bit Ciphers:**

```nginx
# Nginx configuration
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!3DES:!DES';
# Apache configuration  
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:!3DES:!DES
```

**Additional Mitigations:**

* Upgrade to TLS 1.3 which removes 3DES entirely
* Limit connection duration through aggressive rekeying (every 64MB for 3DES)
* Restrict request volume per connection (Apache/Nginx default 100 requests)
* Monitor for excessive traffic patterns indicating potential attacks
* Prioritize AES ciphers over legacy 64-bit alternatives in cipher suite ordering

**Testing Commands:**

```bash
# Test server configuration
openssl s_client -connect example.com:443 -cipher '3DES'

# Verify 3DES is disabled (should fail)
nmap --script ssl-enum-ciphers -p 443 example.com
```