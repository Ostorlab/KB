To mitigate the risk of UBJSON typed-array count marker amplification attacks, apply defence-in-depth controls so that decoding attacker-supplied UBJSON is bounded on byte size, declared count, and nesting, and is unreachable without authentication on public surfaces.

- **Reject UBJSON where it is not a product requirement**: On unauthenticated endpoints (for example a public GraphQL route), reject `Content-Type: application/ubjson` and force JSON-only parsing. This closes the unauthenticated amplifier surface while leaving authenticated routes unaffected if UBJSON support is intentionally retained there.

- **Add an application-level body-size guard before decoding**: Bound `len(request.body)` to a conservative limit appropriate for the schema (for example 256 KiB for a GraphQL query body) before invoking the decoder. Framework caps such as Django's `DATA_UPLOAD_MAX_MEMORY_SIZE` bound the raw byte size, but a far smaller limit is appropriate for structured query bodies.

- **Cap declared counts and nesting**: Reject UBJSON typed-array / typed-object count markers (`#`) whose declared count exceeds the remaining input length (or a sane absolute cap such as `1_000_000`) *before* the decoder iterates. The amplifier's signature is a declared count larger than the remaining payload bytes; reject it at the boundary rather than paying the decode cost.

- **Rate-limit unauthenticated endpoints**: Apply per-IP throttling (for example DRF throttles or edge/WAF rate limits) on public UBJSON-accepting endpoints to bound concurrent amplifier requests.

- **Pin and track the UBJSON library**: Pin the UBJSON decoder dependency (for example `py-ubjson==0.16.1`) and track upstream fixes for typed-array count-vs-input-length validation; consider a stricter JSON decoder if UBJSON is not a product requirement.

=== "Python"

  ```python
  import ubjson
  from django.http import HttpResponseBadRequest

  MAX_UBJSON_BODY_SIZE = 256 * 1024      # 256 KiB; GraphQL bodies are tiny
  MAX_CONTAINER_COUNT = 1_000_000       # reject declared counts above this

  def safe_ubjson_loadb(request) -> dict:
      """Decode a UBJSON request body with size and count guards.

      Raises and returns a 400 *before* the expensive decode loop runs.
      """
      raw = request.body
      if len(raw) > MAX_UBJSON_BODY_SIZE:
          raise ValueError("UBJSON body exceeds size limit.")

      # The amplifier's signature is a typed-array count marker whose declared
      # count exceeds the remaining payload bytes. Reject it at the boundary.
      if _declares_oversize_count(raw, MAX_CONTAINER_COUNT):
          raise ValueError("UBJSON declared count exceeds limit.")

      try:
          data = ubjson.loadb(raw)
      except Exception as exc:
          raise ValueError("Variables are invalid UBJSON.") from exc

      if not isinstance(data, dict):
          raise ValueError("UBJSON body must be a map/object.")
      return data
  ```
