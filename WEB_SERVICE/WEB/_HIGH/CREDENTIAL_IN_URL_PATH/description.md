A sensitive authentication credential (such as an API key or organization key) is passed as a URL path segment instead of an HTTP request header. The path segment is the sole authentication factor: the application resolves the requesting identity directly from it, and no second factor or authentication middleware guards the route.

Because the credential is embedded in the URL, every intermediary that records URLs by design captures the complete, sole authentication token:

- **Reverse-proxy / ASGI-server access logs:** Default `access_log` configurations (nginx, uvicorn, gunicorn) record the full request line, including the path, which contains the credential.
- **Shared / CDN proxy cache keyed by URL path:** When no `Cache-Control: no-store` (or `Vary`) header is set, a path-keyed shared cache may serve one requestor's authenticated JSON/JSON-RPC response (containing organization PII, scans, tickets, etc.) to a different requestor.
- **Browser history / bookmarks:** Any browser-based client or UI recording visited URLs persists the credential in clear text; no source-level mitigation can hide a URL path from history.
- **Referer header:** With no `Referrer-Policy: no-referrer` set, any outbound link or sub-resource load sends the full URL (default `Referer`) to a third-party origin, disclosing the credential.

A single leaked URL therefore enables full impersonation of the credential's scope. When the resolved key has an elevated default role (for example `admin`), the impact is full read and write access to the organization's scans, vulnerabilities, tickets and member PII — effectively an organization-scope account takeover.

This is a source-level design flaw: the credential is bound as a path variable at the routing layer and traverses the raw URL before any per-handler authorization check.

=== "Python"
  ```python
  import starlette.applications
  import starlette.routing

  # The {api_key} path variable IS the sole authentication credential.
  mcp_parent_app = starlette.applications.Starlette(
      routes=[
          starlette.routing.Mount(
              "/apis/mcp/{api_key}",
              app=mcp_app.streamable_http_app(),
          )
      ],
      lifespan=lifespan,
  )
  ```

=== "Request"
  ```http
  POST /apis/mcp/<organization_api_key> HTTP/1.1
  Content-Type: application/json

  {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"me","arguments":{}}}
  ```

=== "Leakage vector"
  ```text
  # Default reverse-proxy access log line captures the full, sole credential:
  10.0.0.1 - - [21/Jul/2026:11:50:01 +0000] "POST /apis/mcp/<organization_api_key> HTTP/1.1" 200 1234
  ```
