The **`Cross-Origin-Embedder-Policy`** (COEP) HTTP response header configures the current document's policy for loading cross-origin resources that are requested in `no-cors` mode (images, scripts, styles and other subresources embedded by a typical page). Without an enforcing COEP header, a document loads cross-origin resources **whether or not those resources have consented to being embedded**: by default resources behave as if they carried `Cross-Origin-Resource-Policy: cross-origin`, meaning they can be pulled into any origin's page.

### What "missing or invalid" means

* **Missing**: no `Cross-Origin-Embedder-Policy` header is sent on the document response, which the browser treats as the default policy `unsafe-none`.
* **Invalid**: the header carries a value that is not one of the valid tokens, is set more than once, or carries multiple tokens — per the HTML specification this is equivalent to setting `unsafe-none`, so an invalid header has exactly the same effect as a missing one.

Valid tokens are:

* `unsafe-none` — the default; the document may load cross-origin `no-cors` resources without their explicit permission.
* `require-corp` — the document may only load same-origin resources, or cross-origin resources that explicitly permit embedding via the `Cross-Origin-Resource-Policy` (CORP) header or by being requested in CORS mode.
* `credentialless` — cross-origin `no-cors` resources may be loaded without explicit permission, but requests are sent without credentials: cookies are omitted from the request and ignored in the response.

### Impact

* **Cross-origin resource inclusion**: without COEP, a document can embed third-party resources that never opted in to being embedded. This is a building block for `Spectre`-class side-channel attacks, where malicious script in the attacker's origin reads data from resources pulled into the same renderer process, and for cross-site attacks that rely on embedding a victim's authenticated resources.
* **No cross-origin isolation**: COEP (with `require-corp` or `credentialless`) together with `Cross-Origin-Opener-Policy: same-origin` is a precondition for the document to be cross-origin isolated (`window.crossOriginIsolated === true`). Features that depend on cross-origin isolation — such as `SharedArrayBuffer` and unthrottled `Performance.now()` timers — are unavailable without it.

This is a defense-in-depth header: its absence is not directly exploitable on its own, but it removes a layer of process-level isolation that modern browsers provide against cross-origin data leakage.

=== "Bash"
  ```bash
    # Check whether a document response sends a valid COEP header:
    curl -sI "https://example.com/" | grep -i "cross-origin-embedder-policy"

    # No output, or a value other than 'require-corp'/'credentialless'
    # (or a duplicated/multi-token header) -> missing or invalid.

    # Verify the document is actually cross-origin isolated (browser console):
    #   window.crossOriginIsolated   // false when COEP/COOP are not both set
  ```

### Validating and triaging a finding

* COEP is a **document policy**: the header belongs on top-level HTML document responses (and on framed documents). A missing-COEP finding raised against a JSON API endpoint, a redirect, an image or another non-document resource is a low-actionability instance of the check — remediate it by setting the header on document responses of the scanned origin, not on every response.
* A document that legitimately embeds third-party resources which do not send CORP or CORS opt-ins (legacy maps, analytics beacons, ad frames) cannot enable `require-corp` without breaking those embeds. This is a documented operational constraint, not a false positive: the standard migration paths are the `crossorigin` attribute (to switch the embed to CORS mode), `credentialless` (to load without credentials), or `Cross-Origin-Embedder-Policy-Report-Only` for a staged rollout. An informed decision to stay on `unsafe-none` for a specific document should be recorded as an accepted risk for that document, not treated as a scanner error.
* The header complements COOP, CORP and CSP — check them together, since they compose into the resource-isolation posture of the site.
