To mitigate BREACH attacks, implement the following strategies:

**Primary Mitigations:**

1. **Disable HTTP Compression for Sensitive Pages** - Turn off gzip/deflate for responses containing secrets and compress static assets only, not dynamic content with secrets.

2. **Separate Secrets from User Input** - Ensure that sensitive data never appears in the same HTTP response as user-controlled input. Use separate endpoints for sensitive operations that don't echo user input.

3. **Randomize Secrets Per Request** - Generate new CSRF tokens frequently and rotate session identifiers regularly to limit the window of opportunity for attackers.

**Implementation Examples:**

```nginx
# Disable compression for sensitive endpoints
location /api/csrf { gzip off; }
location /user/ { gzip off; }
```

```python
# Flask: Disable compression middleware
app.config['COMPRESS_MIMETYPES'] = []

# Django: Remove GZipMiddleware from MIDDLEWARE setting
MIDDLEWARE = [
    # ... other middleware, but NOT:
    # 'django.middleware.gzip.GZipMiddleware',
]
```

**Additional Defenses:**

* Add random padding to responses containing secrets
* Implement rate limiting (10 requests per minute for user input endpoints)
* Monitor for suspicious request patterns indicating potential attacks
* Use double-submit cookie CSRF protection methods