The implementation is secure; the numeric type constraint prevents script-delimiting
characters from reaching the `loadUrl` URL, so no change is required for security.

As defense-in-depth (not required for security), the following low-effort hardening reduces
reliance on implicit behavior:

- Construct the URL with `Uri.Builder` / `appendQueryParameter` so encoding is explicit and
  self-documenting instead of relying on raw string-template interpolation.
- Add an explicit host allow-list in `shouldOverrideUrlLoading` so the `WebView` only navigates
  to the expected origin, preventing any future navigation to arbitrary hosts.
- Keep the interpolated fields typed as numeric primitives (`Int`/`Double`); do not regress them
  to `String`. A type-check lint rule or unit test asserting the numeric type guards against
  future regressions.
- Run a sink scan for `addJavascriptInterface`, `evaluateJavascript`, `loadData`, and
  file-scheme overrides in CI to ensure none are introduced on this `WebView` instance.

To close the residual server-side reflection surface, request the backend team verify that the
rendered page HTML-encodes the query parameter values when reflecting them.
