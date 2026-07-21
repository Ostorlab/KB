Do not let the HTTP client forward a custom authentication header across redirects unattended. Treat any non-standard header that carries a credential (`X-API-Token`, `X-Api-Key`, `X-Auth-Token`, ...) as sensitive and re-validate every redirect hop before re-attaching it.

Apply the following, in order of preference:

* **Disable automatic redirect-following** on the request that carries the credential (`allow_redirects=False`), then follow redirects manually and re-attach the custom header **only** to a trusted-host allowlist, dropping it for any other host (including storage/CDN hosts the upstream may redirect to).
* **Re-validate each hop**: before following a `3xx`, parse the `Location`, confirm the scheme is `https` and the hostname is in an allowlist, and strip the custom header on any host-change or `https -> http` downgrade. Reuse existing SSRF helpers (`is_private_ip` / `validate_webhook_endpoint`) if the project already provides them.
* **Scope the credential to the trusted host only**: a redirect is a trust boundary; a credential issued for `api.example.com` must never be sent to any other host.
* **Pin the HTTP client version** so the redirect header-stripping behaviour is deterministic across deployments, and add a regression test asserting the custom header is **not** forwarded across a cross-host `3xx` and across an `https -> http` downgrade.

As a defence-in-depth measure, prefer the standard `Authorization` header (which mainstream libraries strip on host-change) over custom headers for service-to-service authentication where the upstream accepts it.
