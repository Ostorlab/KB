Bind the inbound HMAC to the request body and per-request freshness before performing any object lookup or state-changing sink.

* **Body-bound HMAC** — compute `HMAC(SECRET, str(org_id) + "|" + raw_request_body)` (or `HMAC(SECRET, request.body)`) and transmit the signature in a request header (e.g. `X-Webhook-Signature`) rather than embedding a static per-org secret in the URL path. Reject (401/403) on mismatch before any side effect.
* **Replay protection** — require an `X-Webhook-Timestamp` header and reject requests outside a ±5 minute window, plus an `X-Webhook-Nonce` stored in a short-TTL cache to reject duplicates.
* **Bind the object-resolution key** — include the object-resolution key (`issue_key` / `sys_id` / `integrationId` + path params) and any attacker-influenced path values (`ownerName` / `appName` / `build_id`) in the signed material so a leaked URL alone cannot retarget arbitrary objects.
* **Order sinks after authorization** — perform any outbound fetch authenticated with the org's stored credential **after** the signature check, subscription/quota gate, and resource-ownership validation succeed; never before.
* **Rotate secrets** — rotate the shared `SECRET` if any webhook URL may have leaked; rotation invalidates all previously-embedded per-org URL segments.
* **Validate the sender** — if the deployment intends a source-IP allowlist, enforce it against the documented third-party webhook-sender egress ranges (a Host-header validator is not a source-IP firewall).

### Secure shape (Python / Django)

```python
import time
from django.core.cache import cache

def verify_webhook_signature(request, secret, org_id, max_age=300):
    sig = request.headers.get("X-Webhook-Signature", "")
    ts = request.headers.get("X-Webhook-Timestamp", "")
    nonce = request.headers.get("X-Webhook-Nonce", "")
    try:
        ts_int = int(ts)
    except ValueError:
        return False
    if abs(time.time() - ts_int) > max_age:
        return False
    nonce_key = f"webhook_nonce:{org_id}:{nonce}"
    if cache.add(nonce_key, "1", timeout=max_age * 2) is False:
        return False  # replay
    expected = hmac.new(
        secret.encode(),
        f"{ts}:{nonce}:".encode() + request.body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(sig, expected)
```
