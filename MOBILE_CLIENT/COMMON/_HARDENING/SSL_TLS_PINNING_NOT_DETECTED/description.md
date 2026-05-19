The application's HTTPS connections to one or more backend domains were successfully intercepted by a proxy without triggering any certificate rejection, indicating that SSL/TLS certificate pinning is not implemented for those connections.

Without pinning, the application trusts any certificate signed by a CA in the system trust store. An attacker who can position themselves between the device and the server — on a compromised Wi-Fi network, a rogue access point, or a device with a user-installed CA certificate — can silently decrypt all HTTPS traffic, including authentication tokens, session cookies, and sensitive personal data.

**Common attack scenarios:**

- **Corporate proxy / rogue Wi-Fi:** An attacker installs a custom CA on the device (or the user is on a network that does so) and decrypts all HTTPS traffic transparently.
- **Credential theft:** Session tokens and authentication headers are extracted from intercepted requests, enabling account takeover without any visible indication to the user.
- **Data tampering:** Responses are modified in transit to alter application behavior, inject malicious content, or bypass feature flags and entitlement checks.
- **API key extraction:** API keys and secrets embedded in request headers or bodies are harvested, enabling unauthorized access to backend services.
