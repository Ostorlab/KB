A Content Security Policy (CSP) is considered secure when it effectively restricts the sources of content that can be loaded by the browser, thus reducing the risk of attacks like Cross-Site Scripting (XSS). A well-defined CSP includes directives that limit where scripts, styles, and other resources can be loaded from.

A secure CSP might look like this:

```http request
Content-Security-Policy: default-src 'self'; script-src 'self' https://trustedscripts.example.com 'nonce-abcdef'; style-src 'self' 'sha256-xyz'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';
```

This policy allows content only from the same origin and a trusted source while disallowing any embedded objects and framing.