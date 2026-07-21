- __Move the credential out of the URL path into a request header__: The client should send the key as `X-API-Key` (or `Authorization: Bearer <key>`) instead of a path segment, while the route uses a constant path such as `/apis/mcp`.

=== "Python"
  ```python
  import starlette.applications
  import starlette.routing

  # Constant path; the key is read from the X-API-Key header, not the URL.
  mcp_parent_app = starlette.applications.Starlette(
      routes=[
          starlette.routing.Mount(
              "/apis/mcp",
              app=mcp_server.mcp.mcp_app.streamable_http_app(),
          )
      ],
      lifespan=lifespan,
  )
  ```

- __Reject path-supplied keys__: Read the credential from a header instead of `path_params`, and reject any request that supplies the key only in the path.

=== "Python"
  ```python
  def get_auth_context(ctx) -> tuple[...]:
      req = getattr(getattr(ctx, "request_context", None), "request", None)
      api_key = req.headers.get("x-api-key") if req is not None else None
      if not api_key:
          raise AuthenticationError("API Key not provided in X-API-Key header.")
      organization_api_key = up_models.OrganizationAPIKey.objects.get_from_key(api_key)
      return organization_api_key.organisation, organization_api_key
  ```

- __Set `Cache-Control: no-store` and `Referrer-Policy: no-referrer`__ on the route immediately, even before the path redesign lands, to suppress cache and Referer leakage of any still-path-bound keys.

=== "Python"
  ```python
  import starlette.middleware.base

  @starlette.middleware.base.BaseHTTPMiddleware
  async def no_store_headers(request, call_next):
      response = await call_next(request)
      response.headers["Cache-Control"] = "no-store"
      response.headers["Referrer-Policy"] = "no-referrer"
      return response

  # pass middleware=[no_store_headers] to the Starlette(...) constructor.
  ```

- __Apply least privilege__: Make API keys non-admin by default (for example `role` defaulting to `reader`) so a leaked key grants the minimum scope; require explicit elevation for administrative actions.
- __Rotate and revoke__: Until clients migrate, treat any currently-issued path-bound key as potentially exposed. Force-rotate organization API keys and revoke keys found in historical proxy, CDN and browser logs. Configure reverse-proxy access logs to redact the `/apis/mcp/<key>` path segment.
