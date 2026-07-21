HTTP clients that follow `3xx` redirects reuse the headers of the original request when re-issuing the request to the `Location` target. The standard `Authorization` header is stripped by most libraries on a host-change or on an `https -> http` downgrade (the CVE-2018-18074 class), but custom authentication headers such as `X-API-Token`, `X-Api-Key`, `X-Auth-Token`, or any non-standard header carrying a credential are **not** in that strip set. They are therefore forwarded verbatim to whatever host the redirect points at, including cross-host and `https -> http` downgrades, disclosing the credential to the redirect target.

This is a custom-header variant of the CVE-2018-18074 credential-replay class (CWE-200). The defect is deterministic from the source: the application attaches the credential as a custom header on the outbound request and performs no per-hop redirect re-validation, so the custom header survives every redirect the upstream service emits. Whether such a redirect is actually issued by the trusted upstream is a runtime property; the leak materializes only when the upstream replies with a `3xx` to a different host or downgrades the scheme, but the application provides **no** protection against it.

The impact is bounded by the authority of the replayed credential. An integration/API token scoped to a single service (for example a full-access token for an upstream build/release API) carries meaningful backend authority over that service, but is not a master cloud secret or service identity. The path is typically reachable only by an authenticated principal, which further caps the severity; the missing redirect re-validation, however, is a real, source-proven hygiene defect that must be fixed defensively regardless of whether the upstream currently issues such redirects.

=== "Python (vulnerable)"
  ```python
  import requests

  # A full-access API token is attached as a custom header. `requests` only
  # strips the standard `Authorization` header on a host-change redirect
  # (rebuild_auth / should_strip_auth); the custom `X-API-Token` survives
  # every 3xx target, including cross-host and https -> http downgrade.
  def fetch_build(owner, app, build_id, api_key):
      headers = {"Content-type": "application/json", "X-API-Token": api_key}
      return requests.get(
          f"https://api.example.com/v0.1/apps/{owner}/{app}/builds/{build_id}/downloads/build",
          headers=headers,
      )  # allow_redirects defaults to True, up to 30 hops.
  ```

=== "Python (fixed)"
  ```python
  import urllib.parse

  import requests

  TRUSTED_HOSTS = {"api.example.com"}

  def fetch_build(owner, app, build_id, api_key):
      url = (
          f"https://api.example.com/v0.1/apps/{owner}/{app}/builds/{build_id}/downloads/build"
      )
      # Do not let the library auto-follow redirects with the credential attached.
      # Resolve redirects manually and re-attach the header only to trusted hosts.
      while True:
          headers = {"Content-type": "application/json", "X-API-Token": api_key}
          response = requests.get(url, headers=headers, allow_redirects=False)
          if response.is_redirect:
              next_url = urllib.parse.urljoin(
                  response.url, response.headers["Location"]
              )
              if urllib.parse.urlparse(next_url).hostname not in TRUSTED_HOSTS:
                  # Drop the credential before following the redirect.
                  response = requests.get(next_url, allow_redirects=False)
              else:
                  url = next_url
                  continue
          return response
  ```
