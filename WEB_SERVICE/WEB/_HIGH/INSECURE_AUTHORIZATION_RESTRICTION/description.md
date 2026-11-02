Insecure Authorization Restriction refers to weaknesses in server-side restrictions that can be exploited through HTTP request manipulation techniques. This vulnerability allows attackers to bypass access controls, leading to unauthorized access to resources, privilege escalation, and allowing unauthorized users to retrieve, create, update, or delete sensitive data.

Targeting Insecure Authorization Restrictions on a web server, for example, would involve these techniques:

   * **HTTP Request Method fuzzing**: Testing invalid, malformed, or unexpected HTTP methods on the server.
   * **HTTP Request Path fuzzing**: Manipulating the HTTP request path by deforming it, adding to it, or subtracting from it.
   * **HTTP Request Query Parameter fuzzing**: Adding, removing, or changing the original query parameters.
   * **HTTP Request Header fuzzing**: Adding familiar headers, removing headers, or adding proxy headers.

All these techniques target defects, vulnerabilities, or mistakes in a server's logic.

=== "Python"
  ```python
    import requests

    response = requests.get("http://www.some-url.com/unauthorized_path")

    '''if we have some unauthorized path that gets us a 403 code,
    we can try something like adding a query parameter like "debug=true" to see if we can
    trick the server by exploiting some mistake.'''

    response = requests.get("http://www.some-url.com/unauthorized_path?debug=true")

    '''Might get us the resource we want''
  ```

### Distinguishing access-control denials from bot-mitigation challenges

A `4xx` response is only evidence of an authorization restriction when it is produced by the application's own access-control logic. Many hosts are protected by CDN or WAF bot-mitigation features that answer requests with a challenge or block page **before the request reaches the application**. These responses use ordinary client-error status codes (`403`, `429`, `503`), but they are not authorization decisions, and they are issued per request: the same client can receive a challenge for one request and a normal response for the next, depending on the edge location, the cache state or the request's risk score. Observing a status transition from such a response to a `2xx` response is not, on its own, evidence that an access control was bypassed.

Signals that a `4xx` response is a bot-mitigation challenge rather than an access-control denial include:

   * **Vercel**: the `x-vercel-mitigated: challenge` (or `block`) response header, an `x-vercel-challenge-token` header, a `Retry-After` header, or a "Vercel Security Checkpoint" interstitial page.
   * **Cloudflare**: a `cf-mitigated: challenge` response header, or a challenge interstitial page ("Just a moment...", "Checking if the site connection is secure...").
   * **WAF and DDoS protection in general**: an interstitial HTML body unrelated to the application, a security-vendor `Server` header, or a `Retry-After` header.

When validating a reported bypass, check that the evidence excludes these benign explanations:

   * The original `4xx` response carries no mitigation signals. If it does, the subsequent `2xx` response must be attributable to the mutated request element rather than to the challenge simply not being triggered for that request: challenge responses are issued per request and per edge location, so a `2xx` served from a different edge location, or from cache, can occur regardless of any header, path or parameter mutation.
   * The bypassed response serves the same resource with the same semantics — the same path after normalization — and not an error page, a redirect target, or a different resource.
   * The resource is actually restricted by the application. A public resource, such as a static documentation page, has no access control to bypass.