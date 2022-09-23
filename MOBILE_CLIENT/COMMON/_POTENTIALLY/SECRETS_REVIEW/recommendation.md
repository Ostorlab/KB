Sensitive data must not be packaged with the application. If access to this data is required, apply procedures to
securely encrypt, store, and retrieve credentials for your services.

For keys that have a risk of over-billing, ensure the API Key is implementing key pinning or is exposing the service
through authenticated APIs.

Key-pinning restricts usage of the key to the application through cryptographic signature and is a setting to enable
by the service provider, like Google Maps.

For keys that may cause unauthorized access, restrict the permissions and roles to non-critical or expose
the service through an authenticated API.

The API must implement proper access control and rate-limiting and keys should be rotated periodically.
