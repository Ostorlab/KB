# Client-Supplied App Version Trust Not Confirmable

A mobile client commonly reports its own installed application version to a backend endpoint (for example an update-check or heartbeat endpoint) using attacker-mutable HTTP-layer signals, such as an `app_version` query parameter and a matching version header. The backend is expected to use these values to drive security decisions, including whether to force a mandatory application update, gate access to deprecated API behavior, or enable feature flags.

This entry covers the outcome where a focused static source analysis of the mounted client source cannot confirm or refute whether the server trusts those client-supplied version signals over authenticated session or device metadata. The mounted source contains only the client that consumes the endpoint (it builds the request and parses the response); it contains no server-side route, controller, version-comparison, force-update, or feature-gate logic. Because the server-side decision sink is absent from the mounted source, there is no complete attacker-controlled source-to-sink path and no concrete security impact can be proven from the client source alone.

## Client-side trust boundary

The client-side facts that can be proven from the mounted client source are:

- The client sends its application version as a plain query parameter (for example `app_version`), sourced from the device's own `PackageManager.getPackageInfo(...).versionName`. The value is bound verbatim into the request URL with no client-side validation or normalization.
- The same version is sent redundantly as a custom HTTP header (for example `X-App-Version`) by a request interceptor. Both the query parameter and the header are attacker-mutable at the HTTP layer (a request-intercepting proxy or a forged raw request can set either independently).
- The request is issued through an interceptor-bearing HTTP client that also attaches the authenticated principal (for example a Bearer token sourced from encrypted preferences). Depending on the token state, the request may reach the server with or without an authenticated session.
- The client performs no local cross-check between the version query parameter, the version header, and the authenticated session, and no local minimum-version enforcement. The client derives its security decision (for example `mustUpdate = response.isNotEmpty()`) purely from the server response body, fully delegating the decision to the server.

## Why no vulnerability is confirmed

The candidate premise is a server-side trust and business-logic concern. The server-side handler that would read the client-supplied version and decide whether to return a force-update response or gate deprecated behavior is absent from the mounted source. Without that sink there is no complete attacker-controlled source-to-sink path, and no concrete security impact (update-check bypass or deprecated-behavior unlock) can be demonstrated from the client source. No dynamic or live request was issued against a running server, so there is no confirming server response showing a bypass.

Classification: static-only / unresolved. The client-side trust-boundary facts are confirmed; the server-side trust question is not resolvable from this repository alone.
